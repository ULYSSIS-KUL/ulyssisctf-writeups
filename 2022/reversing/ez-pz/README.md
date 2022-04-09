# eZ-pZ writeup

For reference, here's a hexdump of a file with a rather simple flag:

```
$ hexdump -C EZPZ.8XP
00000000  2a 2a 54 49 38 33 46 2a  1a 0a 00 46 55 4c 59 53  |**TI83F*...FULYS|
00000010  53 49 53 20 43 54 46 20  63 68 61 6c 6c 65 6e 67  |SIS CTF challeng|
00000020  65 20 65 5a 2d 70 5a 20  2d 20 73 68 6f 75 6c 64  |e eZ-pZ - should|
00000030  20 62 65 20 65 61 73 79  2c 20 72 69 67 68 74 3f  | be easy, right?|
00000040  00 00 00 00 00 00 ce 01  cc 01 ef 7b cd 28 08 02  |...........{.(..|
00000050  cd 08 08 02 cd d5 a8 d1  f3 01 44 a9 d1 11 b8 a9  |..........D.....|
00000060  d1 21 76 a9 d1 cd d4 a8  d1 11 1a aa d1 21 76 a9  |.!v..........!v.|
00000070  d1 06 31 1a be 20 1e 23  13 10 f8 01 44 a9 d1 11  |..1.. .#....D...|
00000080  e9 a9 d1 21 76 a9 d1 cd  d4 a8 d1 21 76 a9 d1 cd  |...!v......!v...|
00000090  c0 07 02 18 08 21 35 a9  d1 cd c0 07 02 fb c9 c9  |.....!5.........|
000000a0  21 2a a9 d1 01 0b 00 00  11 79 08 d0 ed b0 af 32  |!*.......y.....2|
000000b0  99 05 d0 fd 46 09 fd 4e  1c fd cb 1c b6 fd cb 09  |....F..N........|
000000c0  fe c5 cd 20 13 02 c1 cb  a0 fd 70 09 fd 71 1c 2a  |... ......p..q.*|
000000d0  4e 24 d0 cd e8 0a 02 cd  0c 05 02 38 0f eb cd 9c  |N$.........8....|
000000e0  1d 02 d5 c1 11 44 a9 d1  ed b0 af 12 cd 78 15 02  |.....D.......x..|
000000f0  cd 14 08 02 c9 45 6e 74  65 72 20 6b 65 79 3a 00  |.....Enter key:.|
00000100  4b 65 79 20 69 6e 63 6f  72 72 65 63 74 2e 00 48  |Key incorrect..H|
00000110  65 6c 6c 6f 20 64 65 61  72 20 70 61 72 74 69 63  |ello dear partic|
00000120  69 70 61 6e 74 21 20 54  68 69 73 20 69 73 20 6f  |ipant! This is o|
00000130  6e 6c 79 20 66 69 6c 6c  65 72 20 74 65 78 74 2c  |nly filler text,|
00000140  00 20 62 65 63 61 75 73  65 20 73 6f 6d 65 20 6d  |. because some m|
00000150  65 6d 6f 72 79 20 6e 65  65 64 73 20 74 6f 20 62  |emory needs to b|
00000160  65 20 70 72 65 73 65 72  76 65 64 20 66 6f 72 20  |e preserved for |
00000170  74 65 00 6d 70 6f 72 61  72 79 20 62 75 66 66 65  |te.mporary buffe|
00000180  72 73 2e 00 01 02 03 04  05 06 07 08 09 0a 0b 0c  |rs..............|
00000190  0d 0e 0f 10 11 12 13 14  15 16 17 18 19 1a 1b 1c  |................|
000001a0  1d 1e 1f 20 21 22 23 24  25 26 27 28 29 2a 2b 2c  |... !"#$%&'()*+,|
000001b0  2d 2e 2f 30 06 ca d8 17  ff 7f 00 00 15 a8 5e 6c  |-./0..........^l|
000001c0  e0 7f 00 00 00 00 00 00  00 00 00 00 05 13 40 00  |..............@.|
000001d0  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
000001e0  00 00 00 00 c0 06 ca d8  17 ff 7f 00 00 15 a8 5e  |...............^|
000001f0  6c e0 7f 00 00 00 00 00  00 00 00 00 00 05 13 40  |l..............@|
00000200  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
00000210  00 00 00 00 00 c0 63 99                           |......c.|
```
In this challenge, the participant is given a mysterious `EZPZ.8XP` file. What
on earth is even an `8XP` file? Let's try `file(1)`:

```
$ file EZPZ.8XP
EZPZ.8XP: TI-83+ Graphing Calculator
```

So this is either TI-BASIC code, or Z80 assembly. The
[TI-8x-series](https://en.wikipedia.org/wiki/TI-83_Plus) have a Z80 chip,
Wikipedia happily informs us.

```z80
[0x00000046]> pd
     0x00000046      ce01           adc a, 0x01
     0x00000048      cc01ef         call z, 0xef01
     0x0000004b      7b             ld a, e
     0x0000004c      cd2808         call 0x0828
     0x0000004f      02             ld (bc), a
     0x00000050      cd0808         call 0x0808
     0x00000053      02             ld (bc), a
     0x00000054      cdd5a8         call 0xa8d5
     0x00000057      d1             pop de
     0x00000058      f3             di
     0x00000059      0144a9         ld bc, 0xa944
     0x0000005c      d1             pop de
     0x0000005d      11b8a9         ld de, 0xa9b8
     0x00000060      d1             pop de
     0x00000061      2176a9         ld hl, 0xa976
     0x00000064      d1             pop de
```

That seems to be Z80, except... it doesn't make much sense, as if valid
instructions are interleaved with random bytes that are decoded into silly
instructions (such as the `pop de`).

Trying to actually run the file in an emulator, or trying to transfer it to a
physical device, will result in an error. Why? The actual file contents start
with the bytes '`ef 7b`', which is a "TI Extended BASIC Token", followed by a
token indicating a [TI-84+
CE/CSE](https://en.wikipedia.org/wiki/TI-84_Plus_CE#TI-84_Plus_CE_and_TI-84_Plus_CE-T)
assembly program. Aha! These seem to have an
[*eZ80*](https://en.wikipedia.org/wiki/EZ80) chip, which explains the weird
disassembly, and also the name of the challenge.

Now one might wonder, are there any eZ80 disassemblers or emulators? Neither
IDA, Ghidra, radare2 and binutils support it! But of course there are, namely
[zdis](https://github.com/CE-Programming/zdis) and
[CEmu](https://github.com/CE-Programming/CEmu/) (not to be confused by the
Wii U emulator of the same name).

So woat does the program actually do? It seems to do the following:

1. call the `$020828` and `$020808` system functions (resp. `HomeUp` and
   `ClrLCDFull`)
2. call a subroutine at `$D1A93C`, which seems to set up a prompt and call
   `$021320` (`GetStringInput`), then copy data from the system into a buffer
   included within the program, at `$D1A9AB`. So this subroutine basically reads
   some user input and stores it somewhere.
3. disable interrupts
4. call a subroutine at `$D1A8ED` with pointers to temporary buffers loaded into
   `de`, `ix` and `hl` (the middle one pointing to the user input buffer).
5. compare the contents with one of the other buffers to a hardcoded blob
6. if a comparison fails, print "`Key incorrect.`"
7. if all comparisons succeed, call `$D1A8ED` once more with a slightly different
   set of buffers, and print the contents of the last buffer (i.e. the one
   assigned to `hl`)

It seems that `$D1A8ED` will be the main focus of this challenge, then. From
the two calls, we can derive its signature:

```c
void func_D1A8ED(char* input(de), char* userinput(ix), char* output(hl)) {
	// TODO
}
```

At a quick glance, it becomes clear that the function doesn't like potential
readers: it sets up several CPU control registers (such as `MBASE`), switches
between ADL (eZ80) and MADL (mixed) modes, reads from `(de)` and `(ix)`, and
immediately afterwards does something strange (as shown below), then writes
`a` into `(hl)`, moves the pointers one byte forwards, in a loop of exactly
49 bytes, which is the length of a flag, including the `FLG{}` circumfix.

```z80
  jr $D1A925
D1A900:
  ld hl, $E5A8D1
  ld hl, $E5A8D7
  ld hl, $E5A8E5
  ld hl, $E5A8E7
  ld hl, $E5A8DE
  ; ...
  ret
D1A925:
  call.is $D1A900
```

This snippet calls a sub-subroutine within itself, which loads `hl` a few
times with different values, and then it returns without having done anything
else. This seems strange at first, but note the call instruction used: `call.is`.
Going through [the eZ80 spec](http://www.zilog.com/docs/um0077.pdf), it seems
that this isn't just a regular call, it actually switches the CPU into Z80
compatibility mode! So the `ld hl, ...` sequence must be interpreted as Z80
instead of eZ80. This will cause the `E5` bytes in the `ld` immediates to be
interpreted as separate instructions, as immediates can't be 24 bits wide in
Z80 mode. `E5` turns out to be `push hl`:

```z80
  jr $D1A925
.assume ADL=0
D1A900:
  ld hl, $A8D1
  push hl
  ld hl, $A8D7
  push hl
  ld hl, $A8E5
  push hl
  ; ...
  ret
.assume ADL=1
D1A925:
  call.is $D1A900
```

I.e. the code seems to set up a list of subroutines to return to, then jumps to
the last one. Each of them seem to be doing a simple arithmetic operation on
the `a` register, so they only need to be glued together in the correct order:

```z80
   cp a, $80
   ccf
   rla
   scf
   inc a
   rlca
   xor c
   ccf
   rra
   jr c, 1f  ; this is originally implemented using 'ret c', but due to the way
   xor $80   ; the stack-based gadget mess works, it functions like a jump)
1f:cpl
   mlt bc
   xor c
   rrca
   ret.l
```

`ret.l` will return us back into eZ80 mode. This code basically does the
following computation:

```c
char func_D1A8ED_iter(char a, char b, char c) {
  bit C;

  C = (a - 0x80) & 0x100; // co
  C = ~C; // ccf
  // rla (using verilog-style simultaneous assignment syntax)
  C <- a & 0x80;
  a <- (a << 1) | C;
  C = 1; // scf
  a = a + 1; // inc a
  a = a <<< 1; // rlca
  // xor c
  a <- a ^ c;
  C <- 0; //! note this!
  C = ~C; // ccf
  // rra
  C <- a & 1;
  a <- (a >> 1) | (C << 7);
  // jr c, 1f; xor
  if (!C) a = a ^ 0x80;
  a = ~a; // cpl
  c = (b*c) & 0xFF; // mlt bc
  a = a ^ c; // xor c
  a = a >>> 1; // rrca

  return a;
}
```

Let's recap: `$D1A8ED` performs the above function with `a` from the `de` input
and `c` from `ix` (and `b` the loop counter), with a fixed input in `de` and
the user input in `ix`, and expects the output to be some value. This operation
isn't too hard to reverse, but if a participant would be too lazy, it'd also be
possible to brute-force the solution character-by-character.

Turns out, the expected user input is the flag, as is easily verified by
plugging `FLG{` followed by garbage into it.

When the flag is input correctly into the program, the message
`Congrats, you were able to solve this challenge!` is decrypted and shown to
the user.

------

**NOTE**: There was an issue with the challenge and how encoded/encrypted flags
were generated and embedded into the binary given to participants. However,
entering this corrutped flag would still print the `Congrats, you were able to
solve this challenge!`-message, thus solves could still be verified manually.
