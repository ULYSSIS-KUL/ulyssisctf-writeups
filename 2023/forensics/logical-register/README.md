# logical-register writeup

When we open the given link, we are able to download two files, `ASCII.png` and `logical-register.v`. We first take a look at the png, it contains a table of ASCII characters with their respective positions and addresses. Nothing to special, so we take a look at the .v file. This file contains some sort of programming language!

After some googling we find this language is called verilog. It is a [HDL](https://en.wikipedia.org/wiki/Hardware_description_language) used to program FPGAs. Now that we know what we are looking at, we can start to analyse it. The program starts with the definition of three register arrays: 
```
reg[11:0] ascii [94:0];
reg[11:0] seed  [48:0];
reg[11:0] flag  [48:0];
```
These are arrays of buses, for example `reg[11:0] ascii [94:0];` defines an array with 95 entries of 12 bit buses. 

The next section is called `initial`, some more googling reveals that this is the place where we can define elements which will not be converted to hardware. They are usefull for simulation, so that is probably why they are here. In reality we would get the initial values of the ascii and seed registers from blockmemory. 

Finally we see an `always` section. Bingo, this section will get converted to hardware so this is where the fun stuff happens! We can see the flag gets defined character per character: 
```
flag[0] = ascii[38] | seed[0]; // F
```
What does this mean? Another googling session reveals this line is trying to bitwise or the 39th bus of the ascii array with the first bus of the seed array. This explains the name of this challenge, we are doing logical operations on registers! 

But what should we do with the result of these operations? For this, we can finally make use of the png we got as a part of this challenge! If we look closely we can find out a few things about it. First off, we see that the ascii array is an array with pointers to the address of an ascii character. If we then think about the operation for the first flag character, we notice it has no effect on the pointer. So flag[0] must point to `010010100000` which is the adress of `F`, the first character of almost every flag!

The only thing left to do is perform these bitwise operations 48 more times. 
