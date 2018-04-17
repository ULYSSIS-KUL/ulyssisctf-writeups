# taurinensis

> We have developed a revolutionary encryption algorithm that is [proven to
> be unbreakable](https://en.wikipedia.org/wiki/One-time_pad). We encrypted
> all our trade secrets, [including this PNG file](cipher.png.bin) with it,
> but... we lost the key. Can you help us recover it?

## The concept

Unlike some people thought, we actually used an infinitely-long key. But, when
you'd xor the ciphertext with the PNG header --
`\x89PNG\r\n\x1a\n\x0D\0\0\0IHDR`... -- (i.e. calculating the key), the first few
digits of Pi would appear. Thus, if you xor the whole file with the digits of Pi,
you get the plaintext. This is known as a [known-plaintext
attack](https://en.wikipedia.org/wiki/Known-plaintext_attack).

If you ever see [snake
oil](https://en.wikipedia.org/wiki/Snake_oil_(cryptography)) in the wild,
run as fast as you can and use something better (eg. GnuPG, OTR, LUKS, ...).

(This challenge was in fact inspired by one of these. I can't remember what
exactly it was, though.)

## Example code

```py
#!/usr/bin/env python3

import sys

# generates pi.
# taken from https://rosettacode.org/wiki/Pi#Python because laziness
def keystream():
    q, r, t, k, n, l = 1, 0, 1, 1, 3, 3
    while True:
        if 4*q+r-t < n*t:
            yield n
            nr = 10*(r-n*t)
            n  = ((10*(3*q+r))//t)-10*n
            q  *= 10
            r  = nr
        else:
            nr = (2*q+r)*l
            nn = (q*(7*k)+2+(r*l))//(t*l)
            q  *= k
            t  *= l
            l  += 2
            k += 1
            n  = nn
            r  = nr

# encode keystream
def encKeystr(ks):
    # 2 digits/byte
    itr = ks.__iter__()
    while True:
        a = itr.__next__()
        b = itr.__next__()
        yield (a<<4) | b

# encrypt the plaintext with the given keystream
def enc(plain, key):
    return map(lambda t: t[0]^t[1], zip(plain, key))

# a ^ b = c iff c ^ b = a
# thus, enc(plain, key) == cipher iff enc(cipher, key) == plain
enc(open('cipher.png.bin', 'rb').read(), encKeystr(keystream()))
```

