# arc-zero writeup

We're greeted with a `.sfc` file, of which an example can be found [here
](./arc-zero-example.sfc). The Internet happily informes us that this file is
a ROM for the *Super Nintendo* console (aka the SNES). A very famous emulator
is *bsnes* (and its more complete twin *Higan*), but these lack a debugger.
Luckily, [bsnes-plus](https://github.com/devinacker/bsnes-plus) or [Mesen-S
](https://github.com/SourMesen/Mesen-S) provide full debug features.

[Wikipedia says](https://en.wikipedia.org/wiki/Super_Nintendo_Entertainment_System#CPU_and_RAM)
the SNES has a 65816 CPU, a 16-bit "expansion" of the venerable 6502. In other
words, a rather ugly instruction set. Oh well.

A string in the ROM header, `MBSFXJ`, tells us that this ROM is made using
[libSFX](https://github.com/Optiroc/libSFX). Another string in the file also
points in this direction. That means we can already skip analyzing a lot of
code, as it comes from [here
](https://github.com/Optiroc/libSFX/blob/master/include/CPU/Runtime.s) anyway,
and we can get to the meat of the code:

The main loop simply waits for a (VBlank) interrupt and calls a subroutine,
in a loop:

```
:	wai
	jsr Sub1
	bra :-
```

This subroutine checks the controller inputs and, if `start` is pressed, reads
8 bits from the controller and pushes it to a buffer:

```c
/* lda $4219
 * bit #$10
 * bne :+
 * rts
 * :            */
uint8_t joyh = REG_JOY1H;
if (!(joyh & 0x10)) return
/* and #$0f
 * tax
 * lda $4218
 * stx temp1
 * ora temp1
 * ldx ptr
 * sta 0,x
 * inc ptr
 * bne :+
 * inc ptr+1   */
joyh &= 0xf;
joyh |= JOY1L;
*ptr = joyh;
++ptr;
/*:inc count
 * lda count
 * cmp #$40
 * beq :+
 * rts
 *:           */
++count;
if (count != 0x40) return;
/* lda #<buf
 * sta ptr+0
 * lda #>buf
 * sta ptr+1
 * stz count
 * jmp Sub2   */
ptr = &buf;
count = 0;
Sub2(); // tail call
```

(`ptr` had been initialized to `&buf` at the start of the program.)

What's more, right before `buf` in memory, is the ASCII string `Enter flag
here:`. So, the supplied input must be the flag that we're looking for.

`Sub2` is a bit more involved and does the following things:
1. It copies various data from ROM to various parts of RAM inside the cartridge.
2. It also copies the contents of `buf` into the cartridge RAM.
3. It then... *writes* to cartridge ROM addresses? And polls them and expects
   them to change as well?
4. Once that's done, it copies cartridge RAM back to main RAM, compares it to 
   another block of data, and if so, it jumps to a codepath that sets the
   background color to green and returns right before the string `Congrats, you
   got the flag!`. Otherwise, it jumps to another snippet of code setting the
   background to red instead before returning, with the text `Nope, sorry, try
   again.`.

So what's going on here? Looking around through some [SNES register
documentation](https://problemkaputt.de/fullsnes.htm), it seems that this isn't
merely ROM, but that the code is accessing something called the ***GSU***.
What's that? Well, looking further in that document tells us that is actually
the (in)famous [Super FX](https://en.wikipedia.org/wiki/Super_FX) chip! It
looks like we have been fooled, and that the actual challenge must be in the
Super FX code instead of the 65816 code. The princess is in another castle.
(The Wikipedia article also says that the successor of the Super FX is called
'ARC', which is certainly not a coincidence with this challenge's name.)

Luckily, bsnes-plus also has a Super FX disassembler and debugger, so we can
continue without too much of a hassle. Though, the Super FX instruction set is
rather unusual: nominally it is a RISC, with 16 registers and a load-store ISA.
Though, instead of having wider instruction words, it still uses single-byte
instructions that default to using register `r0`, relying on prefix
instructions to switch to using other registers instead. So what would be
described as eg. `sub r0, r1, r2` is instead implemented as `from r1; to r0;
sub r2`. If the `from` and `to` registers are the same, `with` can be used as a
shorthand. `with` is also used for single-register instructions (eg. `lob`
(16→8 bit conversion) or `ldb (reg)` (8-bit load)). The special combination of
`from` and `with` indicates a move instruction. Other instruction prefixes are
used as well because the default opcode space is rather small. `r12` doubles as
a loop counter register, `r13` is the loop start register, `r14` is the link
register, and `r15` the program counter. It also has a single delay slot.

The Super FX memory map looks like this:
* `+000`: code, 128 bytes
* `+080`: data buffer 1, 64 bytes
* `+0c0`: data buffer 2, 64 bytes
* `+100`: work memory, 256 bytes

The code starts out as follows (after having transformed the code into an
ARM-style syntax):

```c
/* ibt  r9, #0x03f ; load immediate, byte
 * iwt r10, #0x0c0 ; load immediate, word (16-bit)
 * iwt r11, #0x100
 * mov  r0, r11
 * add  r1, r11, r11
 * iwt r13, #:+    ; loop start
 * mov r12, r11    ; loop counter
 *:dec  r0
 * dec  r1
 * stb  r0, [r1]
 * loop
 * stb  r0, [r1]        */
r0 = r11 = 0x100;
r1 = 0x200;
for (int i = r11; i > 0; --i) {
	--r0;
	--r1;
	*r1 = r0;
}
*r1 = r0;
```

This code initializes the work memory with the values `0 1 2 3 4 5 6 ...`.

```c
/* ibt r3, #0
 * ibt r7, #0   */
uint8_t r3 = 0, r7 = 0;
while (true) {
	/*:add r6, r7, r11
	 * and r5, r7,  r9
	 * add r5, r10        */
	r6 = r11 + r7;        // r11 = 0x100
	r5 = r10 + (r7 & r9); // r10 = 0xc0, r9 = 0x3f
	/* ldb r1, [r6]
	 * add r0, r1, r3
	 * ldb r2, [r5]
	 * add r0, r2
	 * lob r0       */
	r0 = (r3 + 0x100[r7] + 0x0c0[r7 & 0x3f]) & 0xff;
	/* add r4, r0, r11
	 * mov r3, r0
	 * ldb r0, [r4]
	 * stb r0, [r6]
	 * stb r1, [r4]      */
	r4 = r11 + r4;       // r11 = 0x100
	r3 = r0;
	*r6 = *r4;
	*r4 = *r1;           // r1 is the old value of *r6
	/* inc r7
	 * cmp r7, r11
	 * bne :-            */
	++r7;
	if (r7 == 0x100) break;
}
```

This may not seem like much to the untrained eye, but this code looks like the
key schedule of [RC4](https://en.wikipedia.org/wiki/RC4), with a key of 64
bytes residing at `+0xc0` and state at `+0x100`. What's more, the code
following this is the PRNG phase of RC4, so there's no doubt left. (And,
"coincidentally", RC4 used to be called *ARC*4, "Alleged RC4", as the name was
trademarked, and the algorithm a trade secret.)

With that sorted out, there's only a small piece of code left, neatly filling
up the remaining available space:

```
   iwt r13, #:+
   mov r12, r9
   add r9, r9         ; r9 = 0x80
:  ldb r0, [r10]      ; r10 was 0xc0 at entry of this snippet
   ldb r1, [r9]
   xor r0, r1
   stb r0, [r10]
   inc r9
   inc r10
   loop
   nop                 ; delay slot
   stop                ; stop GSU, signal 65816 that we're done
   nop                 ; delay slot
```

This code XORs the data at `+0xc0` with the data at `+0x80`. So, let's piece
everything together:

1. The 65816 uploads the GSU code to `+0` in cartridge RAM
1. The 65816 uploads 64 data bytes to `+0xc0` in cartridge RAM
1. The 65816 uploads the user input (64 bytes) to `+0x80` in cartridge RAM
1. The GSU code runs, performing the key schedule using the data at `+0xc0`.
   This data blob is thus the RC4 key.
1. The GSU then generates 64 bytes of PRNG output, also at `+0xc0`.
1. The GSU XORs the input data with the RC4 stream, storing the output at
   `+0xc0`.

Once the GSU has finished, the 65816 is back into play, and compares the result
of the XOR operation with another data block, and displays whether the user has
been successful or not, as explained earlier.

So now we can start working backwards:
* The result is considered correct if the final output is the same as a known
  block of data, i.e. if the latter is the same as the RC4-encrypted input.
* The RC4-encrypted input is the XOR of the user input and the RC4-stream.
* The RC4-stream depends only on the hardcoded key.

Thus, we can satisfy `blob2 == (RC4-stream ^ input)` by supplying
`RC4-stream ^ blob2` as user input. And luckily, with the memory view in
bsnes-plus, this value can easily be computed using your favourite scripting
language. And with the indication in RAM (remember that?), this input must be
the flag. And that's exactly what computing this XOR yields us. (Well, it
yields the flag with the suffix `ARC0 ULYCTF2023` to pad it out to 64 bytes.)

