# clanger writeup

> We have managed to obtain some hardware from Europe's most wanted assassin
> used to encrypt her communications! It seems to contain a secret encrypted
> message, can you manage to decrypt it?

In this message, we are shown a webpage with the following items:

* An RSA public key `(N, e)`
* An RSA ciphertext `ct` being the encrypted flag
* Partial source code of the challenge (an [RSA-CRT
  ](https://en.wikipedia.org/wiki/RSA_(cryptosystem)#Using_the_Chinese_remainder_algorithm)
  implementation)
* Two forms, one for signing arbitrary messages with the same key as the
  encrypted data, one for verifying such signatures
* The knowledge that the message signing is sometimes faulty.

The RSA-CRT implementation code contains the following function

```python
def decrypt(key: PrivateKey, ct: int, perturb: bool = False) -> int:
    m1 = pow(ct, key.dp, key.p)
    m2 = pow(ct, key.dq, key.q)
    if perturb: m1 = perturb_int(m1)

    h = pow(key.qinv * abs(m1 - m2), 1, key.p)
    pt = pow(m2 + h*key.q, 1, key.p*key.q)

    # or equivalently (if 'key' had a 'pinv' field):
    #h = pow(key.pinv * abs(m1 - m2), 1, key.q)
    #pt = pow(m1 + h*key.p, 1, key.p*key.q)

    return pt
```

What's going on here? The function first performs the usual RSA-CRT
computations, but then optionally perturbs part of it.

Well, that's neat and all, but...  what does that actually mean?

Let's try what happens when we have a correct decryption, and an incorrect
decryption (for a fault in `m2`):

```
m1 = ct ** dp mod p      ;;      m1' = PERTURB(ct ** dp mod p)
m2 = ct ** dq mod q

h = q^-1 * (m1-m2) mod q ;;      h' = q^-1 * (m1'-m2) mod q
pt = m2 + h*q mod N      ;;      pt' = m2 + h'*q mod N
```

(Note: you can use the "verify" functionality in the webpage to check whether
at least one of the obtained signatures is correct.)

When subtracting `pt'` from `pt`, we obtain the following:

```
pt - pt' = (m2 - m2) + (h - h')*q mod N
```

i.e. `pt - pt'` is divisible by `q`. Which means, thanks to the [Euclidean
algorithm](https://en.wikipedia.org/wiki/Euclidean_algorithm), one can
efficiently calculte the greatest common divisor (GCD) of `pt - pt'` and `N`,
which in this case is `q`! Factorizing `N` and calculating `d` (the private
exponent) is then a piece of cake:

```
q = gcd(pt - pt', N)
p = N // q
d = pow(e, -1, (p-1)*(q-1))
```

Note that, due to the symmetry of the CRT, it doesn't matter in which half of
the computation the perturbation occurs: due to the identity noted in the
comment of the helper code, `pt - pt'` would then ended up being divisible by
`p` instead, still yielding a factor of `N` when computing the GCD.

Now that we have the private key, we can quickly decrypt the plaintext with the
helper functions from the given Python code.

More details of this specfic attack, commonly called the *Bellcore attack*, can
be found [here
](https://www.cryptologie.net/article/371/fault-attacks-on-rsas-signatures/)
and [here](https://eprint.iacr.org/2012/553).

This challenge illustrates the power of *differential fault analysis* (DFA), a
technique often used in the context of hardware security: faults occuring can
perturb the output of cryptographic algorithms, which can reveal the values of
secret inputs.

This isn't just a hypothetical scenario with cosmic rays, these attacks are
actually used in the real world to attack *embedded systems* trying to keep a
key locked away inside the device. For demonstrations on this, you can see eg.
[this video](https://www.youtube.com/watch?v=eO-ayS4pbLQ) for a basic overview,
or [this blogpost
](https://yifan.lu/2019/02/22/attacking-hardware-aes-with-dfa/) or [this
pastebin](https://gist.github.com/plutooo/733318dbb57166d203c10d12f6c24e06) for
how DFA has been applied to resp. the PlayStation Vita and the Nintendo Switch
(though targetting AES instead of RSA).

"Clanger" is both a UK/AUS slang word for "mistake", and a part of a bell
(another word for 'clapper', or "klepel" in Dutch), thus hinting towards the
*Bell*core differential *fault* analysis attack.

For reference, here's the full solution code:

```python
from math import gcd
from Crypto.Util.number import inverse
from rsacrt import *

# get these from the challenge
N, e = ...
s1, s2 = ...
ENCRYPTED_FLAG = ...

pub = PublicKey(N, e)
p = gcd(abs(s1 - s2), N)
q = N // p
d = inverse(e, (p - 1) * (q - 1))
priv = PrivateKey(p, q, d, *get_crt_params(p, q, d))

flag_pt = decrypt(priv, ENCRYPTED_FLAG)
print(decode_int(flag_pt))
```
