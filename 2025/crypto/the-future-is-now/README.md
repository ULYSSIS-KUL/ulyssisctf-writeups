# the-future-is-now writeup

> We have obtained a time-traveller's encryption box, and it looks like it's
> using some futuristic cipher. Can you break it?
>
> NOTE: this challenge involves a slight amount of brute-force calculation ON
> YOUR MACHINE, though it shouldn't take much more than a minute.


> ### Description
>
> We have intercepted a time traveller, and managed to extract some information
> about the cryptography they use from their devices. It looks like in the
> future, Kyber-1024, a new post-quantum cryptography cipher, is the new
> standard. The last message this traveller sent out, was this:
>
> `LKygSFKug3/QK/5XA7rUAtV1XrHBj61Ae/rW/1jE9YK4Qm/9oS69sHfkZ3JXQ4L0nazkymxeVETeTARfFQwoX3qNqE6JBVoonH9pP+Qavhc=` (base64 of ciphertext data)
>
> We furthermore found their public key ([`A`](./A.npy), [`t`](./t.npy)) and an
> encapsulation key ([`ek.u`](eku.npy), [`ek.v`](ekv.npy)). The numpy version
> used is 2.1.0.
>
> Good luck!
>
> ### Files
>
> Here are some files that may be useful:
>
> * Kyber implementation: [`kyber.py`](./kyber.py)
> * encrypted message generator: [`generate.py`](./generate.py)

This challenge uses the [CRYSTALS-Kyber](https://en.wikipedia.org/wiki/Kyber)
post-quantum-secure asymmetric (aka public-key) cipher. (If you're interested
you can find its full spec
[here](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf). For a more
easily understandable explanation, there's [this
lecture](https://media.ccc.de/v/rc3-2021-cwtv-230-kyber-and-post-quantum).)

According to the standard, it should be used only as a "key encapsulation
mechanism", not an encryption method onto itself. That is, it should only be
used to securely exchange a key for a symmetric cipher. This is also what is
done in the challenge: the attached `generate.py` lists:

```py
kp = kyber.keygen(1024)

sk, ek = kyber.encapsulate(kp.pub)
ct = kyber.encrypt(sk, flag.encode())

with open('ciphertext.bin', 'wb') as f: f.write(ct)
np.save('A.npy', kp.pub.A, allow_pickle=False)
np.save('t.npy', kp.pub.t, allow_pickle=False)
np.save('eku.npy', ek.u, allow_pickle=False)
np.save('ekv.npy', ek.v, allow_pickle=False)
```

The code first uses `keygen(1024)` to generate a Kyber-1024 keypair. It then
uses the `encapsulate()` function to generate a `(symmetric key, encapsulated
key)` pair. The `symmetric key` is used for an AES-OCB3 encryption, but it is
only the `encapsulated key` that should be sent over the wire to the other
party: the public key of this second party is used in this encapsulation
procedure. (`encapsulated key` consists of a `u` and a `v` componenet.)

Using its private key, this second party can then use the `decapsulate()`
function to recover the `symmetric key` from the `encapsulated key`. Which
means, both parties can now use `symmetric key` to encrypt in the regular old
symmetric-key way (which doesn't have many weaknesses against quantum
computers).

So far so good, and this is all supposed to be unbreakable, so where's the hole?

Well, there's this part in [`kyber.py`](./kyber.py):

```py
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
```

I'm not sure if you've noticed but `seed = random.randbytes(2)` seems rather
fishy: it only uses **two bytes of randomness** to generate the full Kyber
keypair, instead of the standard-mandated 32! That is, there are only 65536
possible keypairs that could have been used. This is trivially bruteforceable.

Let's thus write a simple program that does exactly that:

```py
ct = base64.b64decode(b'LKygSFKug3/QK/5XA7rUAtV1XrHBj61Ae/rW/1jE9YK4Qm/9oS69sHfkZ3JXQ4L0nazkymxeVETeTARfFQwoX3qNqE6JBVoonH9pP+Qavhc=')
A = np.load('A.npy')
t = np.load('t.npy')
eku = np.load('eku.npy')
ekv = np.load('ekv.npy')
params = Parameters(4, 2)  # kyber-1024

ba = bytearray(2)
keypair = None
break_outer = False
for j in range(256):
    ba[1] = j
    for i in range(256):
        ba[0] = i

        At, s = kyber.recreate_privkey(ba, params.k, params.eta1)

        if (At[1] == t).all():  #  (At[0] == A).all() and  # found!
            keypair = Keypair(ba, Pubkey(A, t, params), Privkey(s), params)
            break_outer = True
            break
    if break_outer:
        break

assert keypair is not None, "no key found :("

sk = kyber.decapsulate(keypair, KeyEncapsulation(eku, ekv))
flag = kyber.decrypt(sk, ct)
print("flag", flag)
```

We let the program run for a bit, and...

```
$ python solve.py
flag b'FLG{13c9ffaa219ca11650aa3db32a927b047720955a964d}'
```
