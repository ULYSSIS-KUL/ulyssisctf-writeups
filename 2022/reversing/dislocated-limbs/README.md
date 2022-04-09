# dislocated-limbs writeup

We are given an ELF file that seems to ask for an input. The Ghidra disassembly
shows us some code in `main()` that first parses some input, and then performs
a timing attack-resistant comparison:

```c
lVar5 = 0;
lVar6 = 0;
do {
    pcVar2 = local_48 + lVar6;
    pcVar3 = FLAG_7f7e + lVar6;
    lVar6 = lVar6 + 1;
    lVar5 = lVar5 + ((long)*pcVar2 - (long)*pcVar3);
} while (lVar6 != 0x31);
if (lVar5 == 0) {
    uStack80 = 0x3b11c1;
    puts("Flag correct! Congrats!");
    uVar4 = 0;
}
```

The code seems to compare the input (in `local_48`) with a constant
`FLAG_7f7e`... in my case, it's a null-terminated string with value
`FLG{e424904938d4f9cf29a06b128103ea451b8b905e20ad}`. So let's enter it?

```
$ ./dislocated.elf
Enter flag: FLG{e424904938d4f9cf29a06b128103ea451b8b905e20ad}
Incorrect flag.
```

Submitting it to the flagserver doesn't do anything either. So there's
something weird going on here.

Maybe there's another flag in the binary? Except, `strings` reveals there are
65536 of these flags inside the binary! So there must be some trick that should
give us a clue as for which one it actually is...

Would it be anywhere in the code? Contrary to popular belief, the code in an
ELF file doesn't start at `main()`, but instead at `_start`, which initializes
the C runtime and actually passes argc and argv to main, so there could be some
other code modifying which flag variable is actually used in the main code.

Alas, there doesn't seem to be any such code present. Most of it is the
standard glibc overhead, and one unnamed function which is the GOT/PLT function
resolution subroutine, which is part of the standard dynamic linking procedure.
(See [this talk](https://www.youtube.com/watch?v=dOfucXtyEsU) for more info on
the last part.)

However, that video also teaches us about something else that's fun to know
about ELF and the dynamic linking system: the dynamic linker can patch up
arbitrary locations of a file while it is loading that file, using what's
called *relocations*. Could a relocation be used here to change the flag
variable in `main()`?

Let's have a look at the file using `readelf`:

```
Section Headers:
  [Nr] Name              Type            Address          Off    Size   ES Flg Lk Inf Al
  [ 0]                   NULL            0000000000000000 000000 000000 00      0   0  0
  [ 1] .interp           PROGBITS        00000000000002a8 0002a8 00001c 00   A  0   0  1
  [ 2] .note.gnu.build-id NOTE           00000000000002c4 0002c4 000024 00   A  0   0  4
  [ 3] .note.ABI-tag     NOTE            00000000000002e8 0002e8 000020 00   A  0   0  4
  [ 4] .gnu.hash         GNU_HASH        0000000000000308 000308 070048 00   A  5   0  8
  [ 5] .dynsym           DYNSYM          0000000000070350 070350 180240 18   A  6   1  8
  [ 6] .dynstr           STRTAB          00000000001f0590 1f0590 0a0105 00   A  0   0  1
  [ 7] .gnu.version      VERSYM          0000000000290696 290696 020030 02   A  5   0  2
  [ 8] .gnu.version_r    VERNEED         00000000002b06c8 2b06c8 000020 00   A  6   1  8
  [ 9] .rela.dyn         RELA            00000000002b06e8 2b06e8 000108 18   A  5   0  8
  [10] .rela.plt         RELA            00000000002b07f0 2b0808 000078 18  AI  5  23  8
  [11] .init             PROGBITS        00000000002b1000 2b1000 000017 00  AX  0   0  4
  [12] .plt              PROGBITS        00000000002b1020 2b1020 000060 10  AX  0   0 16
  [13] .plt.got          PROGBITS        00000000002b1080 2b1080 000008 08  AX  0   0  8

[...]

Relocation section '.rela.dyn' at offset 0x2b06e8 contains 11 entries:
    Offset             Info             Type               Symbol's Value  Symbol's Name + Addend
00000000002b3dd0  0000000000000008 R_X86_64_RELATIVE                         2b1310
00000000002b3dd8  0000000000000008 R_X86_64_RELATIVE                         2b12d0
00000000002b4048  0000000000000008 R_X86_64_RELATIVE                         2b4048
00000000002b3fc0  0000000100000006 R_X86_64_GLOB_DAT      0000000000000000 _ITM_deregisterTMCloneTable + 0
00000000002b3fc8  0000acad00000006 R_X86_64_GLOB_DAT      0000000000000000 __cxa_finalize@GLIBC_2.2.5 + 0
00000000002b3fd0  0000000200000006 R_X86_64_GLOB_DAT      0000000000000000 __gmon_start__ + 0
00000000002b3fd8  0000000500000006 R_X86_64_GLOB_DAT      0000000000000000 stdout@GLIBC_2.2.5 + 0
00000000002b3fe0  0000000600000006 R_X86_64_GLOB_DAT      0000000000000000 stderr@GLIBC_2.2.5 + 0
00000000002b3fe8  0000000800000006 R_X86_64_GLOB_DAT      0000000000000000 __libc_start_main@GLIBC_2.2.5 + 0
00000000002b3ff0  0000000900000006 R_X86_64_GLOB_DAT      0000000000000000 _ITM_registerTMCloneTable + 0
00000000002b3ff8  0000000c00000006 R_X86_64_GLOB_DAT      0000000000000000 stdin@GLIBC_2.2.5 + 0

Relocation section '.rela.plt' at offset 0x2b0808 contains 5 entries:
    Offset             Info             Type               Symbol's Value  Symbol's Name + Addend
00000000002b4018  0000000300000007 R_X86_64_JUMP_SLOT     0000000000000000 strlen@GLIBC_2.2.5 + 0
00000000002b4020  0000000400000007 R_X86_64_JUMP_SLOT     0000000000000000 fflush@GLIBC_2.2.5 + 0
00000000002b4028  0000000700000007 R_X86_64_JUMP_SLOT     0000000000000000 fgets@GLIBC_2.2.5 + 0
00000000002b4030  0000000a00000007 R_X86_64_JUMP_SLOT     0000000000000000 puts@GLIBC_2.2.5 + 0
00000000002b4038  0000000b00000007 R_X86_64_JUMP_SLOT     0000000000000000 fwrite@GLIBC_2.2.5 + 0
```

There is a `.rela.dyn` section that contains a few relocations that will be
performed once the dynamic linker loads the executable. However, the same video
also told us that the dynamic linker doesn't look at the *section* headers,
but instead uses something called the *program* or *segment* headers. Yes, ELF
files have *two* ways of looking at them, and both store (more or less) the
same data. So, what do we see there?

```
Program Headers:
  Type           Offset   VirtAddr           PhysAddr           FileSiz  MemSiz   Flg Align
  PHDR           0x000040 0x0000000000000040 0x0000000000000040 0x000268 0x000268 R   0x8
  INTERP         0x0002a8 0x00000000000002a8 0x00000000000002a8 0x00001c 0x00001c R   0x1
      [Requesting program interpreter: /lib64/ld-linux-x86-64.so.2]
  LOAD           0x000000 0x0000000000000000 0x0000000000000000 0x2b0868 0x2b0868 R   0x1000
  LOAD           0x2b1000 0x00000000002b1000 0x00000000002b1000 0x00038d 0x00038d R E 0x1000
  LOAD           0x2b2000 0x00000000002b2000 0x00000000002b2000 0x0001b8 0x0001b8 R   0x1000
  LOAD           0x2b2dd0 0x00000000002b3dd0 0x00000000002b3dd0 0x400257 0x400258 RW  0x1000
  DYNAMIC        0x2b2de0 0x00000000002b3de0 0x00000000002b3de0 0x0001e0 0x0001e0 RW  0x8
  NOTE           0x0002c4 0x00000000000002c4 0x00000000000002c4 0x000044 0x000044 R   0x4
  GNU_EH_FRAME   0x2b206c 0x00000000002b206c 0x00000000002b206c 0x00003c 0x00003c R   0x4
  GNU_STACK      0x000000 0x0000000000000000 0x0000000000000000 0x000000 0x000000 RW  0x10
  GNU_RELRO      0x2b2dd0 0x00000000002b3dd0 0x00000000002b3dd0 0x000230 0x000230 R   0x1

[...]

Dynamic section at offset 0x2b2de0 contains 27 entries:
  Tag        Type                         Name/Value
 0x0000000000000001 (NEEDED)             Shared library: [libc.so.6]
 0x000000000000000c (INIT)               0x2b1000
 0x000000000000000d (FINI)               0x2b1384
 0x0000000000000019 (INIT_ARRAY)         0x2b3dd0
 0x000000000000001b (INIT_ARRAYSZ)       8 (bytes)
 0x000000000000001a (FINI_ARRAY)         0x2b3dd8
 0x000000000000001c (FINI_ARRAYSZ)       8 (bytes)
 0x000000006ffffef5 (GNU_HASH)           0x308
 0x0000000000000005 (STRTAB)             0x1f0590
 0x0000000000000006 (SYMTAB)             0x70350
 0x000000000000000a (STRSZ)              655621 (bytes)
 0x000000000000000b (SYMENT)             24 (bytes)
 0x0000000000000015 (DEBUG)              0x0
 0x0000000000000003 (PLTGOT)             0x2b4000
 0x0000000000000002 (PLTRELSZ)           120 (bytes)
 0x0000000000000014 (PLTREL)             RELA
 0x0000000000000017 (JMPREL)             0x2b0808
 0x0000000000000007 (RELA)               0x2b06e8
 0x0000000000000008 (RELASZ)             288 (bytes)
 0x0000000000000009 (RELAENT)            24 (bytes)
 0x000000006ffffffb (FLAGS_1)            Flags: PIE
 0x000000006ffffffe (VERNEED)            0x2b06c8
 0x000000006fffffff (VERNEEDNUM)         1
 0x000000006ffffff0 (VERSYM)             0x290696
 0x000000006ffffff9 (RELACOUNT)          3
 0x0000000000000016 (TEXTREL)            0x0
 0x0000000000000000 (NULL)               0x0
```

Instead of looking at the `.rela.dyn` section, the dynamic linker will read the
tables pointed to by the `RELA` entry of the *dynamic table*!

... and yet, these two have the same address:

> `Relocation section '.rela.dyn' at offset 0x2b06e8 contains 11 entries:`

> `0x0000000000000007 (RELA)               0x2b06e8`

However, there *is* **one** thing that is off: in the dynamic table, the
relocation table is declared to have `288 (RELASZ) / 24 (RELAENT)` entries
(which is 12), while, according to the section headers, the table has only 11
entries! Aha!

... now how do we read this extra relocation to see what it does? We have
several options:

* Use a hex editor: at `0x2b0808+11*24` the following bytes appear:
  `8b 11 2b 00 00 00 00 00 02 00 00 00 a8 03 00 00 fc ff ff ff ff ff ff ff`.
  This is a relocation with target address `0x2b118b`, of type `0x02`
  (`R_X86_64_PC32`), referencing the symbol at index `0x03a8` (936) in the
  symbol table, with addend `-4`. There are two symbol tables, so it could be
  either `FLAG_620f` or `FLAG_63e4`. Only two possible ones left instead of
  65536! Running the binary with either option reveals that in this case, it is
  the second.
* Use a hex editor to add an extra entry to the `.rela.dyn` section in the
  section header table. Look up the offset of the section headers in the main
  ELF header, then change the total size from `0x108` to `0x120`. And suddenly
  the following appears:
  `00000000002b118b  R_X86_64_PC32  0000000000443950 FLAG_63e4 - 4`
* Use `gdb` or another debugger to single-step the program, and print the
  contents of the registers. (Why look at all the ELF stuff when the dynamic
  linker does it for you anyway?) Start the program, pause it when it asks for
  the flag, run `disassemble main`, and then, this pops up:
  `0x0000555555805188 <+248>:  lea  0x1927c1(%rip),%rdi  # 0x555555997950 <FLAG_63e4>`.
* Use [`sstrip`](http://www.muppetlabs.com/~breadbox/software/elfkickers.html)
  to yeet the entire section headers, forcing `readelf`, `objdump`, and all
  reverse-engineering tools to use the `RELA` table from the dynamic table
  instead. Then we can read out the relocation as usual as well.

Reading out the string of that symbol, the verification succeeds and the flag
gets accepted by the flagserver!
