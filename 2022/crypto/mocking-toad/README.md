# Mocking Toad

If we check out the URL that we got, we get some explanation:

```
 The Encryption Toad has stolen my flag :( To tease me, he is giving me encrypted versions of the flag. I did find his code, so maybe that helps me to get my flag back. 
```

The first hyperlink points to `/flag`, where we are greeted with the following JSON:

```
{"iv": "Jdk30LKyLaOlIl21r/gW4w==", "flag": "1SEfNYQSarM9H0la4yYebAr7rU4/9YfxfkUO0/JCOfjI7COHR72DKgxSKVoKH0L+qP9tF2c5fWWLiRDZ6uJAOw=="}
```

It appears we are getting the flag, but it is encrypted and encoded in base64. Decoding results in random, useless gibberish. The mention of an IV ([Initialization Vector](https://en.wikipedia.org/wiki/Initialization_vector)) indicates that this is most likely a [block cipher](https://en.wikipedia.org/wiki/Block_cipher). That's all we have at the moment, so let's check out the code.

The first thing we learn, is that we have AES-CBC encryption. This confirms our idea that we're dealing with a block cipher.

Apart from the endpoints `/`, `/flag` and `/code.py` which we already know, we find another endpoint `/decrypt`. That sounds useful! The endpoint only accepts POST requests. We start with an empty body, but the server crashes. This could be interesting, but for the sake of it, let's try some other inputs. When entering the exact JSON we got earlier, we get a `200 OK`, but the server sadly doesn't give us the decrypted value. If we modify the flag (anywhere except the last two `=` signs, that would result in invalid base64), we get a `400 Bad request`, and the encryption toad is mocking us that we can't even provide a valid input.

Now that we know what we have, let's go back to the aforementioned Wikipedia pages to see if they mention something about vulnerabilities in this kind of encryption scheme. We find two that appear reasonably likely:

* Properties of an IV depend on the cryptographic scheme used. A basic requirement is uniqueness, which means that no IV may be reused under the same key. For block ciphers, repeated IV values devolve the encryption scheme into electronic codebook mode: equal IV and equal plaintext result in equal ciphertext. In stream cipher encryption uniqueness is crucially important as plaintext may be trivially recovered otherwise.
* Some modes such as the CBC mode only operate on complete plaintext blocks. Simply extending the last block of a message with zero-bits is insufficient since it does not allow a receiver to easily distinguish messages that differ only in the amount of padding bits. More importantly, such a simple solution gives rise to very efficient padding oracle attacks.

When we refresh the page that gives us the flag, we sadly see that the IV changes every time. The code also confirms that the `encrypt()` function generates a cryptographically secure IV every time. So let's read a bit about [padding oracle attacks](https://en.wikipedia.org/wiki/Padding_oracle_attack). A perceptive player who knows Dutch might at this point be hinted that he's on the right track by the name of the challenge: the "toad" refers to a vulnerability regarding the "pad"ding. Haha. That was silly.

A very good introduction regarding padding oracle attacks can be found [here](https://robertheaton.com/2013/07/29/padding-oracle-attack/). Assuming that this is not the first CTF to use a padding oracle attack, we can also just search for solutions of other people. We find [this one](https://eugenekolo.com/blog/csaw-qual-ctf-2016/), which links to [this helpful library](https://github.com/mwielgoszewski/python-paddingoracle). Based on the examples we have, we can create our own code to crack this challenge. We like Python 3 way better than Python 2 of course, so to run the code below, you should fix the `paddingoracle` library to be python 3 compatible.

```python
from paddingoracle import BadPaddingException, PaddingOracle
from base64 import b64encode, b64decode
import requests

HOST = 'http://localhost:8000/'

iv = ''


def bytes_to_b64(b):
    return b64encode(b).decode('utf8')


class PadBuster(PaddingOracle):
    def __init__(self, **kwargs):
        super(PadBuster, self).__init__(**kwargs)

    def oracle(self, data, **kwargs):
        print("[*] Trying: {}".format(b64encode(data)))

        r = requests.post(f'{HOST}decrypt', json={'iv': bytes_to_b64(iv), 'flag': bytes_to_b64(data)})

        # The code tells us the status code is 400 for incorrect values, and 200 for correct values.
        if r.status_code == 400:
            print("[*] Padding error!")
            raise BadPaddingException
        else:
            print("[*] No padding error")


if __name__ == '__main__':
    data = requests.get(f'{HOST}flag').json()
    iv = b64decode(data['iv'])
    flag = b64decode(data['flag'])
    padbuster = PadBuster()

    # Block size is always 16 for AES-CBC encryption
    value = padbuster.decrypt(flag, block_size=16, iv=iv)

    print('Decrypted: %s => %r' % (flag, value))
```

When we let it run for a few minutes, it spits out the flag:

```
Decrypted: b'\xdaE\xe1\xed\xc0\xb8D\xec\x10\n\xf5\xa9_o\x8d1\xdf\xbb\xe5\x85?u\x9c.\xff\x92\x7f\x15-k\xbfE\xc7\xd2\x08\x81\x03.\x97\xf4\xea\x89\xe1!8\xe3\xc5\xb9\x94\x07eT\x06\x07}\xda\x9e\x1a\xb3HG\x8c\xa69' => bytearray(b'FLG{aa71234626765d24703e150e07d8d1a9d4f021b32c2f}\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f')
```
