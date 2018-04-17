# Tweaked AES
> 128-bit AES isn't secure enough, so we made it better.
> We're certain this version is still resistant to all known-plaintext and known-ciphertext attacks,
> so you will not be able to crack this.
>
> T = 128-bit random tweak
>
> Ek = standard AES block encrypt
>
> Dk = standard AES block decrypt
>
> Block encryption function: $`E(x) = E_k(T \oplus E_k(x))`$
>
> Block decryption function: $`D(x) = D_k(T \oplus D_k(x))`$

[server](server.py)

## Write-up
You were given a server that could encrypt and decrypt blocks of data according to an AES-based
encryption scheme. On top of the (unknown) 128-bit AES key, the scheme uses a 128-bit "tweak".
Upon connection, the server shows the encrypted flag along with the tweak that was used to encrypt.

Encryption happens in three steps:
1. AES block encryption
2. XOR with the provided tweak
3. Another round of AES block encryption

Decryption needs to undo these three steps, so:
1. AES block decryption (undo encryption step 3)
2. XOR with the provided tweak
3. Another round of AES block decryption (undo encryption step 1)

The AES key is fixed (but randomized for each connection). The tweak can be modified dynamically,
however, any attempts to decrypt the flag with the tweak that was used to encrypt it, are thwarted
by the server!

Luckily, it is possible to work around this restriction by realizing you could change the tweak of
encrypted data by repeatedly decrypting and encryption with specifically crafted tweaks!

$`D_{T=0}(E_{T=Tflag}(D_{T=0}(flag)))`$

$`    = D_k(0 \oplus D_k(E_k(Tflag \oplus E_k(D_k(0 \oplus D_k(flag))))))`$

$`    = D_k(0 \oplus Tflag \oplus 0 \oplus D_k(flag))`$

$`    = D_k(Tflag \oplus D_k(flag))`$

$`    = D_{T=Tflag}(flag)`$

This approach shows that it is possible to decrypt the flag without being blocked from decrypting.

Decrypting a one-block flag might look like this:

```
Tweak used: 9892e3020188df1b95ee159fddd13950
Encrypted flag: ddd3c3eb316bb86b63ed9034a53cb1c5
> decrypt 00000000000000000000000000000000 ddd3c3eb316bb86b63ed9034a53cb1c5
Decrypted message: b77185767d026607c25d1fd0bc05bfd9
> encrypt 9892e3020188df1b95ee159fddd13950 b77185767d026607c25d1fd0bc05bfd9
Encrypted message: acaa1ace60178a9ba5225331ce969105
> decrypt 00000000000000000000000000000000 acaa1ace60178a9ba5225331ce969105
Decrypted message: 466c616767794d63466c616766616365
> exit
Goodbye!
```

```python
from binascii import unhexlify
print(unhexlify('466c616767794d63466c616766616365'))
# b'FlaggyMcFlagface'
```
