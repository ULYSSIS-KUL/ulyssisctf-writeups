
import kyber
import numpy as np

def gendata(flag):
    kp = kyber.keygen(1024)

    sk, ek = kyber.encapsulate(kp.pub)
    ct = kyber.encrypt(sk, flag.encode())

    with open('ciphertext.bin', 'wb') as f: f.write(ct)
    np.save('A.npy', kp.pub.A, allow_pickle=False)
    np.save('t.npy', kp.pub.t, allow_pickle=False)
    np.save('eku.npy', ek.u, allow_pickle=False)
    np.save('ekv.npy', ek.v, allow_pickle=False)

