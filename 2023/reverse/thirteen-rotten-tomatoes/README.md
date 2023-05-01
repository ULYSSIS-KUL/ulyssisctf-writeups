# thirteen-rotten-tomatoes writeup
As said in the flavortext, the file you download is a binary executable. So when executing this, we are greeted with the following message:

```
This program outputs many tomatoes!
Though there are many rotten, but only one fresh.
Can you find the fresh one using the right argument?

Nope, this is the wrong argument.
```

This indicates that the solution to this challenge is to find the right argument for the binary. This can be found through reverse engineering.

There are many different kind of software for reverse engineering binaries like [Ghidra](https://github.com/NationalSecurityAgency/ghidra), [radare2](https://github.com/radareorg/radare2), etc. You should be able to find the solution with most of them. For simplicity I will use my radare2, as it is the one I use most.

Starting of you can find some basic information about the binary with the command `rabin2 -I tomatoes`. This will for example tell us that it is a 32-bit ELF file, and that it is written in C. These are the most interesting things here so let's continue on! Now we will enter the radare2 framework using `r2 tomatoes`, which brings us to the entrypoint of the executable. We can start off by doing a general analysis with `aaa`.

As we got a message about a wrong argument, it is most likely we will receive something similar when we enter the right argument so let's take a look a the strings using `fs strings; f`. This outputs the following code:

```
0x00002008 36 str.This_program_outputs_many_tomatoes_
0x0000202c 50 str.Though_there_are_many_rotten__but_only_one_fresh.
0x00002060 54 str.Can_you_find_the_fresh_one_using_the_right_argument__n
0x00002096 9 str.Success_
0x0000209f 28 str.Here_is_the_flag:_FLG_s_n_n
0x000020bc 35 str.Nope__this_is_the_wrong_argument._n
```

As expected we can see that the program will output some new strings if we would be able to enter the correct argument. Unfortunately for us the flag is still obfuscated (we wouldn't make it this easy ;) ). Radare2 also provides a better way to view the strings using `iz`, which outputs the following:

```
[0x00001090]> iz
[Strings]
nth paddr      vaddr      len size section type  string
―――――――――――――――――――――――――――――――――――――――――――――――――――――――
0   0x00002008 0x00002008 35  36   .rodata ascii This program outputs many tomatoes!
1   0x0000202c 0x0000202c 49  50   .rodata ascii Though there are many rotten, but only one fresh.
2   0x00002060 0x00002060 53  54   .rodata ascii Can you find the fresh one using the right argument?\n
3   0x00002096 0x00002096 8   9    .rodata ascii Success!
4   0x0000209f 0x0000209f 27  28   .rodata ascii Here is the flag: FLG{%s}\n\n
5   0x000020bc 0x000020bc 34  35   .rodata ascii Nope, this is the wrong argument.\n
```

Next we might want to look at the main fuction of the binary. We will use `s main` in radare2 to jump to the main fuction. To try and understand what happens in the main function, we will need to use radare2 disassembler. There are multiple ways to view disassembly in radare2 using both the command `pdf` and `VV`. The latter has a nicer visualisation, but for reasons of simplicity I will stick to `pdf`. In the output of the disassembly we can see many different things, but what we are looking for especially is a function:

```
0x000013dd      e813ffffff     call sym.fruit
│       │   0x000013e2      83c410         add esp, 0x10
│       │   0x000013e5      85c0           test eax, eax
│      ┌──< 0x000013e7      0f84c1000000   je 0x14ae
│      ││   0x000013ed      83ec0c         sub esp, 0xc
│      ││   0x000013f0      8d8398e0ffff   lea eax, [ebx - 0x1f68]
│      ││   0x000013f6      50             push eax
```

The function fruit is most definitely a custom function. Let us take a look at it: `s sym.fruit`. This brings us to the function called "fruit", which is were some interesting things seem to happen. First of all we notice another function called "sym.rot13". The name of the challenge "thirteen-rotten-tomatoes" was an obvious hint to this [algorithm](https://en.wikipedia.org/wiki/ROT13). It is clear now that this algorithm plays a vital role in the challenge. When looking closer at the disassembly, we also see a string being coppied with right underneath we also see a new string recognized by radare:

```
0x0000131f      c7856fffffff.  mov dword [s2], 0x616d6f54  ; 'Toma'
0x00001329      c78573ffffff.  mov dword [var_8dh], 0x73656f54 ; 'Toes'
```

just above the call for the rot13 function, which will take the string "TomaToes" and shift it using the ROT13 algorithm. Followed by that we see another function called "sym.imp.strcmp" which will most likely compare the ROT13 string to something else (perhaps the argument given to the binary!!). Now let us see what "TomaToes" is under the ROT13 cipher: `GbznGbrf`. If we now execute the binary with `./tomatoes GbznGbrf`, we will get the fresh tomato!

```
Success, you found the fresh tomato!
Here is the flag: FLG{}
```
