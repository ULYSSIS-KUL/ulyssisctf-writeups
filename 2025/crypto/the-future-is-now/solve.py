
import base64
import numpy as np
import kyber
from kyber import Parameters, Pubkey, Privkey, Keypair, KeyEncapsulation

if __name__ == '__main__':
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

