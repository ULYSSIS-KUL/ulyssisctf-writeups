# ghost-in-the-rom writeup

We are given a ROM image for the GameBoy Advance, and we are told to run it
using [mGBA](https://github.com/mgba-emu/mgba/releases). Okay, let's do that,
then.

Upon launching, we are greeted with the following screen:

![A crack intro-style animation with a twister and scrolltext and some small
ornaments. The background is a "synthwave sunset"-style thing.](./screenshot.png)

It looks like we're greeted with a demoscene intro! While it looks neat, there
isn't much to be seen. The scrolltext still reassures us that there must be a
flag in the file, though...

([The soundtrack](https://www.pouet.net/prod.php?which=65391#c726712) is a
ProTracker MOD arrangement by AcidPhreak, of the soundtrack of the demo
"Jupiter 666 Video Computer System" by Hackers, which you can watch [here
](https://www.youtube.com/watch?v=GJHjkphr72o)).

So let's dig a little deeper. mGBA has tools for inspecting the current frame,
palette, tiles, backgrounds, and sprites. Hm, wait, what's [the etymology of
that word](https://en.wikipedia.org/wiki/Sprite_(computer_graphics)#Home_systems) again?

> The term was derived from the fact that sprites, rather than being part of
> the bitmap data in the framebuffer, instead "floated" around on top without
> affecting the data in the framebuffer below, much like a ghost or "sprite".
> By this time, sprites had advanced to the point where complete
> two-dimensional shapes could be moved around the screen horizontally and
> vertically with minimal software overhead.

So, the name must have been a hint as for where to look! So, let's open the
sprite view:

![The mGBA sprite view: on the bottom, a list of all sprites is visible, while
at the top, we can see the details of one sprite, such as its graphics data,
position, blend mode, and so on.](./spriteview.png)

What can we see in this list? Well, sprite 64 is quite flickery, and forms the
base of the twister effect. Sprites 18..20 form the `C T F` overlay on the
twister, and the sprites afterwards make up the scrolltext seen on screen. But,
there does seem to be an extra set of sprites, from 0 to 17, that also contain
some data. And if you look closely, it's repeating, and starts with `FLG{`...

Thus, by periodically pausing the emulator (Ctrl+P) and writing down the
corresponding characters yields the flag.
