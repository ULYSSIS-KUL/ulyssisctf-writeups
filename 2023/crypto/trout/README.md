# trout writeup

We are given a web interface that asks us to enter a series of bytes
(base64-encoded) that hash to a specific value:

> Here's a challenge:
> `0066c792f2fcfec284405d4a243b746c368789373e0c16c04e33918d1c88e003`. What's
> that? That, my dear friend, is a SHA256 hash. And you are the one who needs
> to find a value that hashes to it! Good luck. Oh, also, you should have a
> look at the binary linked below.

Well, let's have a look at the binary. Ghidra gives us the following
decompilation:

```c
int main() {
	pcVar3 = getenv("HASH");
	if (pcVar3 == NULL) {
		fwrite("Please give me a HASH environment var!able!\n",1,0x2c,stderr);
		return 1;
	}

	cVar1 = hexdec(local_1e8,pcVar3,0x20);
	if (cVar1 == 0) {
		fwrite("Malformed challenge hash, must be hex-formatted SHA256 hash.\n",1,0x3d,stderr);
		return 1;
	}
	pcVar3 = fgets(local_128,0xff,stdin);
	if (pcVar3 != local_128) {
		fwrite("Could not read input.\n",1,0x16,stderr);
		return 1;
	}

	sVar4 = strlen(local_128);
	cVar1 = hexdec(local_1a8,local_128,sVar4 >> 1);
	if (cVar1 == 0) {
		fwrite("Malformed input, must be hex-formatted.\n",1,0x28,stderr);
		return 1;
	}

	sha256_init(auStack600);
	sha256_update(auStack600,local_1a8,sVar4 >> 1);
	sha256_final(auStack600,local_1c8);
	iVar2 = strncmp(local_1c8,local_1e8,0x20);
	if (iVar2 == 0) {
		pcVar3 = getenv("FLAG");
		printf("Success! Your flag is %s!\n",pcVar3);
	} else {
		puts("Hashed input doesn\'t match challenge hash...");
	}

	return 0;
}
```

The program performs some basic validation on the inputs, then computes the
hash of the input and compares it to a known hash from the environment. We
could try to find some sort of buffer overflow vulnerability, or an
implementation error in the SHA256 code, but luckily, there's a much easier way
to solve this.

Note that the program uses `strncmp` to compare the final values. What does this
function do? Let's look at the manpage:

> ## NAME
>
> `strcmp`, `strncmp` - compare two strings
>
> ## SYNOPSIS
>
> ```c
> #include <string.h>
>
> int strcmp(const char *s1, const char *s2);
> int strncmp(const char *s1, const char *s2, size_t n);
> ```
>
> ## DESCRIPTION
>
> The `strcmp()`function compares the two strings `s1` and `s2`. The
> locale is not taken into account (for a locale-aware comparison, see
> `strcoll(3)`).  The comparison is done using unsigned characters.
>
> `strcmp()` returns an integer indicating the result of the comparison,
> as follows:
>
> * 0, if the `s1` and `s2` are equal;
> * a negative value if `s1` is less than `s2`;
> * a positive value if `s1` is greater than `s2`.
>
> The `strncmp()` function is similar, except it compares only the first
> (at most) `n` bytes of `s1` and `s2`.

Okay, it compares two strings and return zero if they are equal. Wait,
*strings*? Those are null-terminated in C! So the comparison will end as soon
as the first null byte is found. And, being incredibly lucky, the first byte of
the hash we are supposed to invert actually starts with a null byte!

This means we only need to find some bytes that hash to *any* SHA256 hash that
starts with a null byte! So, let's find one:

```py
import hashlib

for l in range(1, 999):
    for i in range(0, 256**l):
        d = i.to_bytes(l, byteorder='big')
        h = hashlib.sha256(d).digest()
        if h[0] == 0:
            print("got one", ''.join("%02x" % x for x in d), ''.join("%02x" % x for x in h))
            exit(0)
```

The first result is `005c`, which in base 64 is `AFw=`. And lo and behold, the
web form gives us the flag!

This challenge was inspired by the [Trucha
bug](https://wiibrew.org/wiki/Signing_bug) in the Wii, where a very similar
vulnerability broke its RSA verification code. Oops. ('Trucha' is Spanish, and
means 'trout'.) If you want to know more about the security system of the Wii
and how broken it is, we highly recommend watching [this
talk](https://media.ccc.de/v/25c3-2799-en-console_hacking_2008_wii_fail).
