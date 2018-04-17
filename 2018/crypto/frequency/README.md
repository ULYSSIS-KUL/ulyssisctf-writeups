# Frequency
> You've been meaning to apply to a new job at Datacamp, but for some reason all the open positions are encrypted...

## Write-up

The challenge file was the plaintext XORed per byte with a 6-byte key. The resulting encrypted data was then encoded in base64.

Due to the short length of the key, the key and thus the plaintext could be derived by using simple frequency analysis on the ciphertext. Automated tools such as [xortool](https://github.com/hellman/xortool) are able to do this automatically.

Decrypting the ciphertext reveals a Datacamp job listing with the flag appended.

