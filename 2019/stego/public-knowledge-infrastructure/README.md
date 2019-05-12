# public-knowledge-infrastructure writeup

When we visit the homepage of the challenge, we are greeted with a file listing containing a lot of certificates. There also is a `certificates.tar` file that claims to contain all the certificates.

When analyzing the certificates we are given, we notice that most of them are leaf certificates issued to `<something>.public-knowledge-infrastructure.play.ctf.ulyssis.org`.
We can visit those websites, but it appears we are greeted with an untrusted certificate warning. When we click through that warning, we get a BOFH excuse.

Since the description gives a lot of weight to certificates, we take a look at those. We download the certificates archive and start analysing the certificates themselves.

First, we grep for FLG through the certificates. `fgrep FLG *.crt` This does not yield us any results.
Let's go a level deeper, dump the contents of each certificate with `openssl x509 -text -noout -in <file>`. This does not yield a flag either.

A certificate is a blob of base64 encoded data, surrounded with a begin and end marker. Let's try decoding this base64 blob.
You can not pass a certificate to base64 directly, because of the markers.

However, we can create a small pipeline to strip the first and last line off, and then pass it to base64: `cat <file> | head -n-1 | tail -n+2 | base64 -d`

Grepping through this data (take care to use the `--text` flag to interpret binary files as text)

```
$ for cert in *.crt; do cat $cert | head -n-1 | tail -n+2 | base64 -d | grep FLG --text; done
```

This yields a lot of binary garbage which I will not reproduce here, but is also contains the flag in there.
To make it a bit more readable for presentation, you can find a hexdump of an example certificate below:

```
00000000  30 82 02 90 30 82 01 f9  a0 03 02 01 02 02 09 00  |0...0...........|
00000010  a2 76 94 6f 28 37 cb 59  30 0d 06 09 2a 86 48 86  |.v.o(7.Y0...*.H.|
00000020  f7 0d 01 01 0b 05 00 30  51 31 0b 30 09 06 03 55  |.......0Q1.0...U|
00000030  04 06 13 02 42 45 31 10  30 0e 06 03 55 04 0a 0c  |....BE1.0...U...|
00000040  07 55 4c 59 53 53 49 53  31 0b 30 09 06 03 55 04  |.ULYSSIS1.0...U.|
00000050  0b 0c 02 49 54 31 23 30  21 06 03 55 04 03 0c 1a  |...IT1#0!..U....|
00000060  55 4c 59 53 53 49 53 20  69 6e 74 65 72 6d 65 64  |ULYSSIS intermed|
00000070  69 61 74 65 20 43 41 20  58 31 30 1e 17 0d 31 39  |iate CA X10...19|
00000080  30 34 32 32 31 33 31 31  34 31 5a 17 0d 31 39 30  |0422131141Z..190|
00000090  36 31 31 31 33 31 31 34  31 5a 30 46 31 44 30 42  |611131141Z0F1D0B|
000000a0  06 03 55 04 03 0c 3b 63  34 66 38 37 32 2e 70 75  |..U...;c4f872.pu|
000000b0  62 6c 69 63 2d 6b 6e 6f  77 6c 65 64 67 65 2d 69  |blic-knowledge-i|
000000c0  6e 66 72 61 73 74 72 75  63 74 75 72 65 2e 70 6c  |nfrastructure.pl|
000000d0  61 79 2e 63 74 66 2e 75  6c 79 73 73 69 73 2e 6f  |ay.ctf.ulyssis.o|
000000e0  72 67 30 81 9f 30 0d 06  09 2a 86 48 86 f7 0d 01  |rg0..0...*.H....|
000000f0  01 01 05 00 03 81 8d 00  30 81 89 02 81 81 00 e0  |........0.......|
00000100  6e b2 57 8d 6a e8 14 c6  46 4c 47 7b 62 35 65 39  |n.W.j...FLG{b5e9|
00000110  65 66 34 35 62 38 66 38  63 31 33 64 34 36 31 66  |ef45b8f8c13d461f|
00000120  34 39 39 64 36 36 37 33  34 66 31 36 62 34 63 66  |499d66734f16b4cf|
00000130  30 34 31 37 37 63 37 34  7d 98 4d 2e a7 29 aa 09  |04177c74}.M..)..|
00000140  df b2 6a d6 d5 eb 8c 59  b3 d6 e3 b7 62 e5 29 01  |..j....Y....b.).|
00000150  21 81 a4 e2 2b 29 68 b8  b8 13 68 bc 31 03 56 0c  |!...+)h...h.1.V.|
00000160  89 a5 7d 50 84 4e f4 fa  4d 84 75 60 7f 7c c6 34  |..}P.N..M.u`.|.4|
00000170  88 0e c7 cf 4e f2 4f 32  6f 9c b4 a1 f7 32 8f 02  |....N.O2o....2..|
00000180  03 01 00 01 a3 7b 30 79  30 09 06 03 55 1d 13 04  |.....{0y0...U...|
00000190  02 30 00 30 2c 06 09 60  86 48 01 86 f8 42 01 0d  |.0.0,..`.H...B..|
000001a0  04 1f 16 1d 4f 70 65 6e  53 53 4c 20 47 65 6e 65  |....OpenSSL Gene|
000001b0  72 61 74 65 64 20 43 65  72 74 69 66 69 63 61 74  |rated Certificat|
000001c0  65 30 1d 06 03 55 1d 0e  04 16 04 14 f5 6d 9c 63  |e0...U.......m.c|
000001d0  4f b4 6e dc f9 5f 92 bd  6f c3 8e 0d 32 45 0f 77  |O.n.._..o...2E.w|
000001e0  30 1f 06 03 55 1d 23 04  18 30 16 80 14 d1 fc 0c  |0...U.#..0......|
000001f0  94 da 18 02 4a a4 e0 08  19 d4 8b e0 7d c6 80 7b  |....J.......}..{|
00000200  a6 30 0d 06 09 2a 86 48  86 f7 0d 01 01 0b 05 00  |.0...*.H........|
00000210  03 81 81 00 8f 79 44 dd  14 dd a7 ec b4 fa c7 e8  |.....yD.........|
00000220  a0 8f 6e f1 a6 b6 d2 2b  66 f2 41 1d 6b ef e7 88  |..n....+f.A.k...|
00000230  cc a6 39 7b fc 0a 2c 1f  1b f4 c9 b7 4e 61 30 51  |..9{..,.....Na0Q|
00000240  83 2f a1 9f 53 f6 7b db  8e c1 1b 00 c5 ad 00 26  |./..S.{........&|
00000250  68 58 21 d2 17 19 a6 b1  ed 37 af 4f 1a c9 02 49  |hX!......7.O...I|
00000260  93 70 71 22 be df ca 30  e4 7c e2 61 b4 15 44 75  |.pq"...0.|.a..Du|
00000270  68 ac 39 c7 a0 b3 23 32  d6 9f 6e a5 ad 42 b3 e8  |h.9...#2..n..B..|
00000280  7b cb 7e d9 1e 0c 70 7f  ce 9e c4 9a 68 2e 64 8c  |{.~...p.....h.d.|
00000290  68 28 e7 4f                                       |h(.O|
00000294
```

