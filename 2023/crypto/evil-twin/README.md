# evil-twin

> Europe's most wanted assassin has managed to escape us so far, but this time
> we are very close to catching her! We have intercepted some of her
> communications, however, it seems to be encrypted with RSA-2048. Luckily, one
> of our spies on the field has informed us that their cryptosystem uses
> something called an "evil twin". Can you help us decrypt her message? RSA
> public key, and just used the same prime twice.

We are given an `output.txt` file which looks like this:

```
n = 8656763867710332576078805237377123609353352070492871620074672545779379068593440552229452780430178193632475912452041221855752697609239008467765277113931123049238571988449001780668019998239122033205718843213835347177276149951353718243184717314347126191007250955633146822593359101327237680977021027196707030544629944276639329712898359188724240970133157330740665051827301518787804375879105808577806681417693318724645057385516340361484069225711648514465559425446452761154151108543960951994273601084394075251831821175533799666114513895076911892914509656148903425026286100240546134968915925379886070411862544235957894841603
e = 65537
# Bytes are converted to integers (and vice-versa) in big-endian manner...
c = 2347232094776487217772876833576792717942164499890027931771852827450527900409852395465614254177020382512561801365962137549685034007641228219777117412531955663163036613468839883911012144958068479262558175152446423459062772330300447780781582179947022231220748545368428967171067968933456158706585825217357023598798345720692397652213428128748848036116374625798631709604281517689430537150136135254701734666464382660594277399772181294766371061364956007524164405359849406038224358247164375080652213288349152169088556230710953846869864201433988126434542368861778663843389144855299742033774597473382530178397879843874333814642
```

Here, `n` corresponds to the RSA modulus, `e` is the public exponent, and `c`
is the ciphertext we need to decrypt. So, how do we decrypt this?

The challenge mentions "evil twins". Given the context of RSA and its use of
prime numbers, this probably refers to [twin
primes](https://en.wikipedia.org/wiki/Twin_prime).

In RSA, `n` is the product of two prime numbers, `p` and `q`. If these are
prime numbers, then there exists a number `m` such that `p=m+1` and `q=m-1` (or
vice versa), which implies `n` must be equal to `m²-1`.

Similarly, `d` is the modular inverse of the public exponent `e`, modulo `φ(n)`
where `φ` is the [Euler totient
function](https://en.wikipedia.org/wiki/Euler%27s_totient_function). If `n` is
a product of two primes `p` and `q`, then `φ(n)` is equal to `(p-1)*(q-1)`,
which in our case is equal to `m*(m-2)`.

Thus, given `n`, we can add one to it and calculate the square root to find
`m`. From this, we can calculate `φ(n) = m*(m-2)`, and thus also the private
exponent `d = e^-1 mod m*(m-2)`. Recovering the plaintext is then a simple
matter of raising `c` to the power of `d` modulo `n`. Or, in Python:

```python
import math

m = math.isqrt(n + 1)
phi = m * (m - 2)
d = pow(e, -1, phi)
pt = pow(c, d, n)
print(pt.to_bytes(49, byteorder='big'))
```

Running this gives us the flag:

```
$ python3 output.txt
b'FLG{7e3d0e84cff88dedfe18aef6834eebff8c72e2721d10}'
```
