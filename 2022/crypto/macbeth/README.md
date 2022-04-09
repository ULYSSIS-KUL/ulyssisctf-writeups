# macbeth
> The NSA suffered a data breach! A long-time NSA employee [REDACTED] turned out to be a spy for the New World Order. She managed to steal top secret information before they exposed her true intentions, and uploaded this data to a free encryption website: Macbeth. We'd really like to know what secrets the NSA wants to hide from us, so could you try to decrypt her stolen information?

## Write-up
We start by going to the Macbeth website mentioned in the challenge description. The UI seems very simple: there is a text box containing some data (which seems to be Base64), as well as an Encrypt and Decrypt button.

Because this is a crypto challenge, we need to know the algorithm details. Our first instinct is to look at the website source. There, we find the following comment:
```
<!-- TODO: remove the /src.zip -->
```

Indeed, when we visit `/src.zip`, we can download the source code for the challenge! Now the real challenge starts...

Looking at the source code, we see three global variables:
```
$zero_iv = pack("H*", "00000000000000000000000000000000");
$k = file_get_contents("/key");
$secret = file_get_contents("/secret");
```

The first global variable seems to be a byte array of length 16 containing all null bytes. The second global variable is a key of some sorts, and the third global variable is another kind of secret.

The source code also defines two functions: `enc($input)` and `dec($input)`. It looks like these functions perform all the cryptographic operations, and they even contain some very useful comments!

### Encryption
According to the code and comments, `enc` does the following:
* Decode the input from Base64 to bytes
* Create a random IV `$iv` (initialization vector) for Rijndael
* Encrypt the input in CBC mode using the global key `$k` and the IV `$iv`
* Compute a MAC value of the IV and ciphertext, again in CBC mode using the global key `$k`, but only keeping the last 16 bytes
* Output the IV, ciphertext, and MAC in Base64

A quick google search tells us that Rijndael is just AES, which is pretty standard for a crypto challenge and very secure. We can also look up the [Wikipedia page for CBC mode](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Cipher_block_chaining_(CBC)). This tells us a ciphertext is encrypted as follows:
```
C_0 = IV
C_i = E_k(P_i XOR C_{i - 1})
```

But what the hell is a MAC? [Wikipedia](https://en.wikipedia.org/wiki/Message_authentication_code) says this:
```
In cryptography, a message authentication code (MAC), sometimes known as a tag, is a short piece of information used for authenticating a message. In other words, to confirm that the message came from the stated sender (its authenticity) and has not been changed. The MAC value protects a message's data integrity, as well as its authenticity, by allowing verifiers (who also possess the secret key) to detect any changes to the message content.
```

OK, so we now know that the MAC can be used to make sure a message was actually encrypted by the server, and not just some random input. In this case, the MAC is computed as follows (here `0` denotes a 16-byte block of zeroes):
```
D_0 = 0
D_1 = E_k(IV XOR D_0) = E_k(IV)
D_i = E_k(C_i XOR D_{i - 1})
M = D_n
```
Remember, the MAC value is computed over the concatenation of `IV` and `C`. Thus, the first input block will be the IV, and the following ones will be the ciphertext blocks. The MAC value `M` is the last block of the CBC encryption.

### Decryption
Now, let's take a look at the decryption function. This function does the following:
* Make sure the input isn't the same as the `$secret`
* Decode the input from Base64 to bytes
* Compute a MAC of the IV and ciphertext in CBC mode using the global key `$k`
* Make sure the computed MAC equals the provided MAC
* Decrypt the ciphertext and output the plaintext in Base64

CBC decryption is performed as follows:
```
C_0 = IV
P_i = D_k(C_i) XOR C_{i - 1}
```

### Solving the challenge
It seems like the `$secret` is quite important here. In fact, the challenge description mentions the NSA secrets, so this ciphertext might be the encrypted flag!

We could try to solve this challenge by slightly modifying the `$secret` ciphertext (e.g. by adding some random bytes to the end). Then, we could simply provide this input to `dec` and the check would be bypassed:
```
    if ($input === $secret) {
        // We shouldn't decrypt the secret...
        return FALSE;
    }
```

However, because of the MAC, we can't just input any ciphertext; we need to know the secret key `$k` to compute a valid MAC value. Or can we? The [Wikipedia page for CBC-MAC](https://en.wikipedia.org/wiki/CBC-MAC) mentions a spectacular attack when the same key `$k` is reused for both CBC encryption/decryption and CBC-MAC. Unfortunately, this attack only seems to work when "encrypt-and-MAC" is used, but in this application the more secure "encrypt-then-MAC" is used...

### Forging a MAC value
Still, we can devise an attack to forge a MAC value. Remember that we can use the website to both encrypt (using `E_k`) and decrypt (using `D_k`) anything, except for the original secret ciphertext. Let `||` denote the concatenation of two blocks.

Suppose the plaintext secret `P` consists of two blocks: `P` = `P_1 || P_2` (this attack could be extended to more blocks). Then `C` looks like this:
```
C_1 = E_k(P_1 XOR IV)
C_2 = E_k(P_2 XOR C_1)
C = C_1 || C_2
```
And `M` looks like this:
```
M = E_k(C_2 XOR E_k(C_1 XOR E_k(IV XOR 0)))
```

Now, let's say we wanted to find a MAC value `M'` for `C'`, with `C'` consisting of three blocks: `C' = C'_0 || C`. In other words, `C'_0` is some ciphertext block which did not occur in the original ciphertext `C`. Then `M'` would look like this:
```
M' = E_k(C_2 XOR E_k(C_1 XOR E_k(C'_0 XOR E_k(IV' XOR 0))))
```

This value of `M'` will be our target MAC value. If we could find `M'`, we could ask the server to decrypt `C'` and obtain the plaintext secret.

Let's start by looking at what happens when we ask the server for the encryption of `C` itself:
```
C''_1 = E_k(C_1 XOR IV'')
C''_2 = E_k(C_2 XOR C''_1) = E_k(C_2 XOR E_k(C_1 XOR IV''))
```
`C''_2` looks very similar to `M` and `M'`, but there's still some blocks missing. Apart from `C`, we also know `IV`, so what happens if we ask the server for the encryption of `IV || C`?
```
C''_0 = E_k(IV XOR IV'')
C''_1 = E_k(C_1 XOR C''_0) = E_k(C_1 XOR E_k(IV XOR IV''))
C''_2 = E_k(C_2 XOR C''_1) = E_k(C_2 XOR E_k(C_1 XOR E_k(IV XOR IV'')))
```
We're very close to `M'`! Unfortunately, we're still missing one block, and the final encryption should contain a `0` block. We can't rely on `IV''` as this value is randomly generated by the server. But perhaps we can still find a way to force the last encryption to contain a `0` block. Let's ask the server for the encryption of `0 || IV || C`.
```
C''_{-1} = E_k(0 XOR IV'')
C''_0 = E_k(IV XOR C''_{-1}) = E_k(IV XOR E_k(0 XOR IV''))
C''_1 = E_k(C_1 XOR C''_0) = E_k(C_1 XOR E_k(IV XOR E_k(0 XOR IV'')))
C''_2 = E_k(C_2 XOR C''_1) = E_k(C_2 XOR E_k(C_1 XOR E_k(IV XOR E_k(0 XOR IV''))))
```
Now `C''_2` is identical to `M'`, with `C'_0` equal to `IV` and `IV'` equal to `IV''`! In other words, `C''_2` is a valid tag for the message `C' = IV || C` with IV value `IV''`. We now have all the tools needed to recover the secret plaintext:
* Let `IV` and `C` be the IV and ciphertext of the secret plaintext
* Ask the server to encrypt `0 || IV || C`, and obtain `IV''`, `C''`, and a MAC value `M''`
* Construct `C' = IV || C`
* Ask the server to decrypt `C'` with IV `IV''` and MAC value `C''_n` (the last block of `C''`)
* The plaintext contains the flag!

### Alternative solution: CBC-MAC length extension
This challenge also has an alternative solution, based on a length extension. Again, observe that the MAC `M` of the encrypted secret looks like this:
```
M = E_k(C_2 XOR E_k(C_1 XOR E_k(IV XOR 0)))
```

Now, let us ask the server for the encryption of `M`. Because `M` is only one block, there will be only one ciphertext block:
```
C' = E_k(E_k(C_2 XOR E_k(C_1 XOR E_k(IV XOR 0))) XOR IV')
   = E_k(IV' XOR E_k(C_2 XOR E_k(C_1 XOR E_k(IV XOR 0))))
```

This ciphertext block is equivalent to the MAC of the ciphertext `C_1 || C_2 || IV'` with IV `IV`. In other words, we computed a valid MAC value for an extended ciphertext. We can then ask the server to decrypt this new ciphertext with the IV `IV` and the valid MAC value to obtain the plaintext with the flag.

This is called a [length extension attack](https://en.wikipedia.org/wiki/Length_extension_attack) and is often applied to hash functions.
