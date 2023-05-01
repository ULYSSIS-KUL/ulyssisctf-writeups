# fair-dice-roll writeup

> Welcome to DSA Signature Service. Here, you may sign or verify arbitrary
> messages with our exclusive DSA keypair.
>
> However, there is one caveat: we do not allow you to sign the message "`We
> will now give you the FLAG`", as we do not plan on doing so. Not adding this
> check would be disastrous, right?
>
> We at DSA Signature Service commit to full transparency, therefore you can
> find our source code, DSA parameters, and public key at the bottom of this
> page.

We are greeted with a web interface that lets us sign and verify messages using
[DSA, the Digital Signature Algorithm](https://en.wikipedia.org/wiki/Digital_Signature_Algorithm).
We can download a small DSA Python library, as well as the public key used. It
seems that SHA3-256 is used as hash function.

The main setup of the challenge seems to be to somehow craft a signature for
the message `We will now give you the FLAG`. How can this be done?

As the Wikipedia article suggests at the bottom of the page, and as [the name
of the challenge alludes to](https://xkcd.com/221/), not using a different
random nonce every time while encrypting allows one to derive the *private* key
used. This is pretty bad!

The Wikipedia article continues with the fact that the PS3 was vulnerable to
this sort of attack. You can find a presentation about it [here
](https://media.ccc.de/v/27c3-4087-en-console_hacking_2010), and it includes
the necessary mathematics to derive the private key, about 35 and a half
minutes in. (Otherwise, reading the Wikipedia article and thinking a bit will
lead you to the same conclusion.)

So, let's try implementing just that. Let's first gather some sample signatures:

```python
p=134407350592998267863958748496786427038365241342687020374161599431997859494523801942847511191758329548349485448433174266456241489004988265221676825188160529471412065981132863735169842745408968304032356780303986455329601050750060090777660801862942433989146941044589739205348552225156026252248587055720251156723
q=1078856157200703665090235253819774846541297242231
g=100879840820109035653436944389958725698669356403282909762447619167500526927050621673087466973457064689115921865277801035053445357650398318816045087030038636064751555750488404435085545767973648355909298430494287590957956431727731328598447740972510275156817205757610536503828758865197391154481691855906460535867
y=132291229603894933602158662558202861373014529346489015468245369823160927863356700939586884214607480671907911601778334767600463997752519374611878155620300750173582655159744015326613603656558219560518116837140972219814032835638643723814675626787342735181408519523452754711515638771947176659113028456633187934728

h1=97209382914815556489208131820973481301209884072167663202143505594784658307816
r1=761409033570077848310535573993515976694832662086
s1=555574392098565200184845694748541548178316191858

h2=57910703576958691507258236810788376244427073126755768575451420724891812285835
r2=761409033570077848310535573993515976694832662086
s2=965429460438481676547797587199171935199614936534
```

The video presentation uses regular division notation, but DSA works in finite
fields, so this is actually *modular* division. We need to multiply `h1 - h2`
with the modular inverse of `s1 - s2` mod `q`. This gives us the nonce `k`.

Once we have obtained the nonce, we can simply undo the "sign" formula from the
DSA Wikipedia page: subtract `h1` from `k*s1`, and multiply with the modular
inverse of `r1` mod `q`. Or, in Python (`invmod` and `priv2pub` come from the
library code given with the challenge to the participants):

```python
k = ((h1 - h2) * invmod(s1 - s2, q)) % q
x = ((k*s1 - h1) * invmod(r1, q)) % q
y_calc = priv2pub(params, x)
assert y == y_calc
```

When running this, the calculated `y` does seem to correspond with the one in
the given data. Oh no...

Now we can simply use the `sign` function from the DSA library:

```python
msg = b"We will now give you the FLAG"
params = p, q, g
h, r, s = sign(msg, params, x, random.randrange(2, q))
assert verify(params, y, (h, r, s))
print("OK")
```

Here, we do actually use a random number as nonce, *as one should*. The
assertion succeeds, so putting `h`, `r` and `s` back into the web form, we are
indeed given the key.

```
h 5988180926790389377565420891347171865747618127086302221772458237655320146566
r 879075454698850940804461730755716664038624895385
s 388747298339784372035668361380384620440510211089
OK
```

Nonce reuse: it's bad. Don't do it.
