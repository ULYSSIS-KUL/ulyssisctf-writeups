
import random
from typing import NamedTuple, Tuple
import numpy as np


__all__ = [
    'Poly', 'Vec', 'Mtx', 'SymmetricKey',
    'Parameters', 'Pubkey', 'Privkey', 'Keypair', 'KeyEncapsulation',
    'keygen', 'recreate_privkey', 'encapsulate', 'decapsulate', 'encrypt', 'decrypt'
]


KYBER_N = 256
KYBER_Q = 3329
KYBER_HALFQ = (KYBER_Q + 1) // 2
KYBER_ETA2 = 2
KYBER_PLAINTEXT_SIZE_BYTES = 32
KYBER_DTYPE = np.int32


Poly = np.array  # a polynomial is an np.array of shape (KYBER_N,) and integer dtype
Vec = np.ndarray # a vector is an np.ndarray of shape (KYBER_N, k) and integer dtype (vector of polynomials)
Mtx = np.ndarray # a matrix is an np.ndarray of shape (KYBER_N, k, k) and integer dtype (matrix of polynomials)
SymmetricKey = bytes  # symmetric key is a `bytes` with length `KYBER_PLAINTEXT_SIZE_BYTES`

class Parameters(NamedTuple):
    k: int
    eta1: int

class Pubkey(NamedTuple):
    A: Mtx
    t: Vec
    params: Parameters

class Privkey(NamedTuple):
    s: Vec

class Keypair(NamedTuple):
    seed: bytes
    pub : Pubkey
    priv: Privkey
    params: Parameters

class KeyEncapsulation(NamedTuple):
    u: Vec
    v: Poly


###############################################################################


def poly_add(a: Poly, b: Poly) -> Poly:
    #assert a.shape == b.shape, (a.shape, b.shape)
    return (a + b) % KYBER_Q
def poly_sub(a: Poly, b: Poly) -> Poly:
    #assert a.shape == b.shape, (a.shape, b.shape)
    return (a - b) % KYBER_Q
def poly_mod_xn1(a: np.array) -> Poly:  # polynomial mod x^n+1, input is larger than Poly
    r = np.array(a, a.dtype)
    #assert r.dtype == a.dtype and r.shape == a.shape
    for i in range(KYBER_N, r.shape[0]):
        r[i - KYBER_N] -= r[i]
    return r[:KYBER_N]
def poly_mul(a: Poly, b: Poly) -> Poly:
    # polynomial multiplication (schoolbook method, not using fancy fast
    # techniques like the NTT here. sorry for slowness.) TODO NTT!
    prod = np.convolve(a, b) % KYBER_Q
    return poly_mod_xn1(prod)

def vec_add(a: Vec, b: Vec) -> Vec:
    #assert a.shape == b.shape, (a.shape, b.shape)
    return (a + b) % KYBER_Q
def vec_mul(a: Vec, b: Vec) -> Poly:  # inner product
    #assert a.shape == b.shape, (a.shape, b.shape)
    result = np.zeros(a.shape[0], dtype=a.dtype)
    for i in range(a.shape[1]):
        prod = poly_mul(a[:,i], b[:,i])
        result = poly_add(result, prod)
    return result

def mtx_mul_vec(A: Mtx, v: Vec) -> Vec:
    #assert A.shape[:2] == v.shape, (A.shape, v.shape)

    result = np.zeros(v.shape, dtype=v.dtype)
    for i in range(A.shape[2]):
        result[:,i] = vec_mul(A[:,:,i], v)

    return result
def mtx_transpose(A: Mtx) -> Mtx:
    return np.transpose(A, axes=(0,2,1))

###############################################################################

def bytes2bits(bs: bytes) -> Poly:
    arr = np.zeros((len(bs), 8), dtype=bool)
    bs = np.array(list(bs))
    for i in range(8):
        arr[:,i] = (bs & (1 << i)) != 0
    return arr.astype(KYBER_DTYPE).reshape((len(bs)*8,))

def bits2bytes(bits: Poly) -> bytes:
    assert len(bits.shape) == 1 and (bits.shape[0] & 7) == 0, bits.shape
    bits = bits.reshape((bits.shape[0] // 8, 8)).astype(KYBER_DTYPE)
    for i in range(1, 8):
        bits[:,0] |= bits[:,i] << i
    return bytes(list(bits[:,0]))  # yes you need the extra list() here or it breaks

###############################################################################

def recreate_privkey(seed: bytes, k: int, eta1: int) -> Tuple[Tuple[Mtx, Vec], Vec]:
    nprand = np.random.Generator(np.random.PCG64DXSM(list(seed)))

    A = nprand.uniform(0, KYBER_Q, (KYBER_N, k, k)).astype(KYBER_DTYPE)
    s = nprand.uniform(0,    eta1, (KYBER_N, k   )).astype(KYBER_DTYPE)
    e = nprand.uniform(0,    eta1, (KYBER_N, k   )).astype(KYBER_DTYPE)
    t = vec_add(mtx_mul_vec(A, s), e)

    return ((A, t), s)

def keygen(bits):
    paramdict = {  #     k  e1
        512 : Parameters(2, 3),
        768 : Parameters(3, 2),
        1024: Parameters(4, 2)
    }

    params = paramdict.get(bits, None)
    if params is None:
        raise ValueError("No Kyber-%d variant exists!" % bits)

    seed = random.randbytes(2)
    At, s = recreate_privkey(seed, params.k, params.eta1)

    return Keypair(seed, Pubkey(*At, params), Privkey(s), params)

###############################################################################

def encaps_inner(A: Mtx, t: Vec, eta1: int, pt: bytes) -> KeyEncapsulation:
    assert len(pt) == KYBER_PLAINTEXT_SIZE_BYTES
    seed = random.Random(pt).randbytes(32)  # don't use plaintext itself as seed directly but hash it first lmao
    nprand = np.random.Generator(np.random.PCG64DXSM(list(seed)))

    r    = nprand.uniform(0, KYBER_ETA2, (KYBER_N, t.shape[1])).astype(KYBER_DTYPE)
    err1 = nprand.uniform(0,       eta1, (KYBER_N, t.shape[1])).astype(KYBER_DTYPE)
    err2 = nprand.uniform(0,       eta1, (KYBER_N,           )).astype(KYBER_DTYPE)

    u = vec_add(mtx_mul_vec(mtx_transpose(A), r), err1)
    v = poly_sub(poly_add(vec_mul(t, r), err2), bytes2bits(pt) * KYBER_HALFQ)

    return KeyEncapsulation(u, v)

def encapsulate(pubkey: Pubkey) -> Tuple[SymmetricKey, KeyEncapsulation]:
    pt = random.randbytes(32)
    return (pt, encaps_inner(pubkey.A, pubkey.t, pubkey.params.eta1, pt))

###############################################################################

def decapsulate(keypair: Keypair, ct: KeyEncapsulation) -> SymmetricKey:
    mn = poly_sub(ct.v, vec_mul(keypair.priv.s, ct.u))
    center = np.abs(KYBER_HALFQ - mn)
    data = np.zeros((*mn.shape, 2), dtype=mn.dtype)
    data[:,0] = mn
    data[:,1] = KYBER_Q - mn
    bound = np.min(data, axis=1)

    pt = bits2bytes((center < bound).astype(ct.v.dtype))

    u2, v2 = encaps_inner(keypair.pub.A, keypair.pub.t, keypair.params.eta1, pt)
    if (ct.u != u2).any() or (ct.v != v2).any():
        raise ValueError("invalid ciphertext!")

    return pt

###############################################################################

def getAES():
    try:
        from Crypto.Cipher import AES
        return AES
    except ImportError:
        from Cryptodome.Cipher import AES
        return AES

def encrypt(key: SymmetricKey, pt: bytes) -> bytes:
    AES = getAES()
    aes = AES.new(key, AES.MODE_OCB)
    ct, tag = aes.encrypt_and_digest(pt)
    assert len(tag) == 16
    assert len(aes.nonce) == 15

    return tag + aes.nonce + ct

def decrypt(key: SymmetricKey, ct: bytes) -> bytes:
    assert len(ct) >= 16+15

    tag = ct[0:16]
    nonce = ct[16:(16+15)]
    ct = ct[(16+15):]

    AES = getAES()
    aes = AES.new(key, AES.MODE_OCB, nonce=nonce)
    return aes.decrypt_and_verify(ct, tag)

###############################################################################

if __name__ == '__main__':
    from datetime import datetime, timedelta

    random.seed(0xdeadbeef)
    # first run to check for correctness, and also JIT/cache the code so the
    # subsequent timings are at least vaguely indicative of the actual speed
    keypair = keygen(512)
    pt, ct = encapsulate(keypair.pub)
    pt2 = decapsulate(keypair, ct)
    assert pt == pt2, "oops, your code isn't working!"

    message = '🩵🩷🏳️‍⚧️🩷🩵'.encode()
    assert len(message) == 32
    assert decrypt(pt, encrypt(pt, message)) == message

    for bits in (512, 768, 1024):
        random.seed(0xdeadbeef)
        print("kyber-%d:" % bits)
        t1 = datetime.now()
        keypair = keygen(512)
        t2 = datetime.now()
        print("\tkeygen", t2-t1)

        t1 = datetime.now()
        pt, ct = encapsulate(keypair.pub)
        t2 = datetime.now()
        print("\tencaps", t2-t1)

        t1 = datetime.now()
        pt2 = decapsulate(keypair, ct)
        t2 = datetime.now()
        print("\tdecaps", t2-t1)

        assert pt == pt2, "roundtrip not OK!"

