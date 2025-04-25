# longcat-is-long writeup

> Here's a rather sizeable cat. But can you make it longer?


> Welcome to ULYSSIS Cloud Compution Solutions vzw. We provide an interface
> to upload and run code on our Cloud Acceleration Platform™, making it run
> much faster than on your pathetic little laptop. However, to ensure the
> security of our incom.. erm, of <i>your</i> data, we require all code you
> upload to be signed using our secret key. We use a proprietary SHA256-based
> message authentication code (MAC), which is proven to be mathematically
> unbreakable.
>
> Good luck!

We are presented with a web interface that, predictable, allows the user to
upload a code snippet (a bash shell script), and run it remotely. The result is
sent back to the user.

The upload form is prefilled with the following example:

```
#MAC:44ed7a0cda6d3f34caefed661cab3ee0ca3a5833467a006074749ed3e3dc93a2
ZWNobyAiVGhlIGxlbmd0aCBvZiB0aGUgZmxhZyBpczogJCh3YyAtYyBmbGFnLnR4dCB8IGF3ayAt
RicgJyAne3ByaW50ICQxfScpIgojIGEgbG9vb29vb29vbmcgY2F0CiNjYXQgZmxhZy50eHQgZmxh
Zy50eHQgZmxhZy50eHQgZmxhZy50eHQgZmxhZy50eHQgZmxhZy50eHQgZmxhZy50eHQgZmxhZy50
eHQK
```

The first line starts with `#MAC:`, which is followed by what looks like the
famous 'proprietary SHA256-based message authentication code' mentioned earlier.
The other lines are base64, and they decode to this:

```sh
echo "The length of the flag is: $(wc -c flag.txt | awk -F' ' '{print $1}')"
# a loooooooong cat
#cat flag.txt flag.txt flag.txt flag.txt flag.txt flag.txt flag.txt flag.txt
```

Running the example yields the following result:

```
Code exited with status 0. Output:

The length of the flag is: 49
```

Any trivial modification to the input will result in the response `MAC
verification failed, sorry.`. Functionally, everything seems to work.

There's one more thing the challenge shows us, and that's the following Python
code:

```python
from typing import *
import codecs, hashlib, hmac


KEY_LENGTH    = 128//8  # need 128 bits security
DIGEST_LENGTH = 256//8  # SHA256 digest bytes
BytesOrArray = Union[bytes, bytearray]


def calc_digest(key: BytesOrArray, data: BytesOrArray) -> BytesOrArray:
    assert len(key) == KEY_LENGTH
    m = hashlib.sha256()
    m.update(key)
    m.update(data)
    return m.digest()


def verify(digest: BytesOrArray, key: BytesOrArray, data: BytesOrArray) -> bool:
    assert len(digest) == DIGEST_LENGTH
    return hmac.compare_digest(digest, calc_digest(key, data))


def format_with_digest(digest: BytesOrArray, data: BytesOrArray) -> BytesOrArray:
    assert len(digest) == DIGEST_LENGTH
    return b'#MAC:%s\n%s' % (codecs.encode(digest, 'hex'), codecs.encode(data, 'base64'))


def extract_digest_and_data(combined: BytesOrArray) -> Tuple[BytesOrArray, BytesOrArray]:
    lines = combined.splitlines()
    macline = lines[0]
    datalines = lines[1:]
    assert macline.startswith(b'#MAC:')
    digest = codecs.decode(macline[5:].strip(), 'hex')
    data = codecs.decode(b'\n'.join(datalines), 'base64')
    return (digest, data)
```

Let's take a closer look at `calc_digest`, which is the code that implements
the MAC: it concatenates the secret key and the input data, then calculates the
SHA256 hash. Reading the corresponding [Wikipedia
article](https://en.wikipedia.org/wiki/SHA-2), it seems that it is vulnerable
to what's called a [Length extension
attack](https://en.wikipedia.org/wiki/Length_extension_attack).

SHA2 and other hash functions using the [Merkle-Damgård construction
](https://en.wikipedia.org/wiki/Merkle%E2%80%93Damg%C3%A5rd_construction) work
as follows: they start off from a constant internal state. They then take this
internal state, along with a part ('block') of the input, and give it to a
"compression function" (typically called `f`). This function outputs a new
internal state. After all input has been processed, the final output state is
the output hash of the hash function.

As this output hash is just the internal state, it's possible for *anyone* to
just keep computing with it, adding more blocks, and still getting a valid
result. In some situations (like non-sensitive integrity checks), that's not
really special. But as soon as part of the input is secret, and nobody is
suposed to generate *new* valid hash outputs, this becomes a really big
problem. In this case, we can just take the example input, append more code to
it (of our choosing!), and derive a new, valid MAC. Oops!

With a tool such as [hlextend](https://github.com/stephenbradshaw/hlextend),
doing this is pretty simple:

```python
import hlextend
from sha2mac import *  # from python code above

ADD = b"\ncat flag.txt\n"  # code that will be appended

inputf = None
with open("example.sh.b64", 'rb') as f: inputf = f.read()

olddigest, data = extract_digest_and_data(inputf)
sha2 = hlextend.new('sha256')
newdata = sha2.extend(ADD, data, KEY_LENGTH, codecs.encode(olddigest, 'hex').decode())
newdigest = codecs.decode(sha2.hexdigest().encode(), 'hex')

with open("output.sh.b64", 'wb') as f: f.write(format_with_digest(newdigest, newdata))
```

We can then upload the newly-generated `output.sh.b64` back in the web
interface, and the verification will be successful, and we now obtain the flag.

