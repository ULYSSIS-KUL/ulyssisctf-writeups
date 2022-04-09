# paintbrush writeup

[Piet](https://esolangs.org/wiki/Piet) is an esoteric programming language that has images as program code.
A Piet program forms a grid of "codels". A codel can be seen as a pixel, but it can be upscaled, so it
might not actually be a pixel. A group of adjacent codels in the same colour is called a colour block.
Colour transitions (based on hue and darkness) decide which  instruction gets executed, as per this table: https://esolangs.org/wiki/Piet#Commands

You received a Piet program with two lines of codels (each codel sized 25x25), looking like this:

![](writeup-example.png)

Running this code using the [npiet](https://www.bertnase.de/npiet/) interpreter shows that the output contains
parts of the flag, but it's clearly not entirely correct or complete:

    ? LG{5? cce2? 1189? 440a? 3453? bd2e? 0e17? 456e? ?

The relevant code is on the first line. The second line only ensures that the code loops back to the first line, following
Piet's rules of how directions change at edges.

If you look at the first line, you can distinguish two patterns: first, there are a lot of red colour blocks, and the number of
codels until the next colour transition varies. Then there are colour blocks in several colours, and each of them only has one codel,
but it's a repeating pattern.

Let's take a look at the red codels first. When those transition into each other, the hue remains the same, only the darkness
changes, from light to darker to darkest to light again. Based on the command table, every such transition leads to a "Push"
instruction, pushing a number on the stack. That number is equal to the number of codels of the previous colour block
(which explains the varying length of the colour blocks). The sequence of red colour blocks pushes the ASCII codes of the
characters of the `FLG{...}` string on the stack. It does this in reverse order, so `F` is on top of the stack after all push
instructions. The last red colour block (before other colours start appearing as well) is only one codel long, because its length
does not have to be pushed on to the stack anymore.

The next pattern is the cycle of light blue -> dark blue -> cyan -> light green -> dark yellow -> red -> light blue.
Most (not all) of those transitions change the hue by 5 steps and the darkness by 2 steps. This translates to the
"output char" instruction, which pops a value off the stack and prints it as a character. This is exactly what we want:
the whole flag is pushed on the stack, so now we want to print it out!

However, two of those transitions do not translate to "output char": light blue -> dark blue does not change the hue,
only the darkness (by two steps), which is the "pop" instruction (just popping a value off the stack, without printing).
Red -> light blue changes the hue by 4 steps and the darkness by 2 steps, which is the "input num" instruction (take a
number as input and push it on the stack). Those instructions prevent the flag from being outputted correctly, we'd want
all colour transitions to translate to the "output char" instruction.

So let's see if the colour cycle can be fixed to achieve that. Red -> light blue is one hue shift too few, so we replace
it by red -> light magenta. This also affects the light blue -> dark blue step, because the light blue became light magenta.
Light magenta -> blue is also a hue change by 5 steps and a darkness change of 2 steps. This means we can change all 9 occurrences
of light blue (#C0C0FF) to light magenta (#FFC0FF) in the image to obtain a Piet program that will correctly output the flag:

    FLG{50cce291189d440a73453dbd2ed0e177456e39def1e1}

