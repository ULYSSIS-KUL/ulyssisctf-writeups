# make-mov-great-again: solution

This is a [MoVfuscated](https://github.com/xoreaxeaxeax/movfuscator) binary,
traditional reversing techniques are of little use here:

```asm
$ objdump -d a.out
; [truncated]
08049584 <main>:
 8049584:       a1 98 81 3f 08          mov    0x83f8198,%eax
 8049589:       ba 84 95 04 88          mov    $0x88049584,%edx
 804958e:       a3 20 80 1f 08          mov    %eax,0x81f8020
 8049593:       89 15 24 80 1f 08       mov    %edx,0x81f8024
 8049599:       b8 00 00 00 00          mov    $0x0,%eax
 804959e:       b9 00 00 00 00          mov    $0x0,%ecx
 80495a3:       ba 00 00 00 00          mov    $0x0,%edx
 80495a8:       a0 20 80 1f 08          mov    0x81f8020,%al
 80495ad:       8b 0c 85 30 26 05 08    mov    0x8052630(,%eax,4),%ecx
 80495b4:       8a 15 24 80 1f 08       mov    0x81f8024,%dl
 80495ba:       8a 14 11                mov    (%ecx,%edx,1),%dl
 80495bd:       89 15 10 80 1f 08       mov    %edx,0x81f8010
 80495c3:       a0 21 80 1f 08          mov    0x81f8021,%al
 80495c8:       8b 0c 85 30 26 05 08    mov    0x8052630(,%eax,4),%ecx
 80495cf:       8a 15 25 80 1f 08       mov    0x81f8025,%dl
 80495d5:       8a 14 11                mov    (%ecx,%edx,1),%dl
 80495d8:       89 15 14 80 1f 08       mov    %edx,0x81f8014
 80495de:       a0 22 80 1f 08          mov    0x81f8022,%al
 80495e3:       8b 0c 85 30 26 05 08    mov    0x8052630(,%eax,4),%ecx
 80495ea:       8a 15 26 80 1f 08       mov    0x81f8026,%dl
 80495f0:       8a 14 11                mov    (%ecx,%edx,1),%dl
 80495f3:       89 15 18 80 1f 08       mov    %edx,0x81f8018
 80495f9:       a0 23 80 1f 08          mov    0x81f8023,%al
 80495fe:       8b 0c 85 30 26 05 08    mov    0x8052630(,%eax,4),%ecx
; [truncated]
```

Let's try something else instead...

```
$ readelf -s a.out

Symbol table '.dynsym' contains 5 entries:
   Num:    Value  Size Type    Bind   Vis      Ndx Name
     0: 00000000     0 NOTYPE  LOCAL  DEFAULT  UND 
     1: 00000000     0 FUNC    GLOBAL DEFAULT  UND sigaction@GLIBC_2.0 (2)
     2: 08049020     0 FUNC    GLOBAL DEFAULT  UND puts@GLIBC_2.0 (2)
     3: 08049030     0 FUNC    GLOBAL DEFAULT  UND exit@GLIBC_2.0 (2)
     4: 08049010     0 FUNC    GLOBAL DEFAULT  UND strcmp@GLIBC_2.0 (2)
```

It wouldn't just compare `argv[1]` with the flag (which is computed at runtime)
using `strcmp`, would it?

```
$ ltrace -bs99 ./a.out h4xx0r
sigaction(SIGSEGV, { 0x8049050, <>, 0, 0 }, nil)
sigaction(SIGILL, { 0x80490d7, <>, 0, 0 }, nil)
strcmp("h4xx0r", "FLG{WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW}")
```

