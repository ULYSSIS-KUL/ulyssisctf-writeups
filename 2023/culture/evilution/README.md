# evilution writeup
In this challenge you are given a .wad file, an extension which you should recognize immediatly. But if not, a quick online search will tell you that a WAD (Where's All the Data?) file contains game data for DOOM.

The logical next step would be to try and play the level included in this WAD file. Luckily, the source code for DOOM was [released in 1997](https://github.com/id-Software/DOOM), giving rise to a rich community of (free and open source) source ports for almost all platforms. [Crispy Doom](https://www.chocolate-doom.org/wiki/index.php/Crispy_Doom) is a source port which sticks as close to the original DOOM as possible, with some minor modernizations such as mouselook.

However, we still need an [IWAD](https://doomwiki.org/wiki/IWAD) to provide the textures and sounds for this level. If you own DOOM, you can just use your DOOM.WAD, but the shareware [DOOM1.WAD](https://doomwiki.org/wiki/DOOM1.WAD) or [freedoom1.wad](https://doomwiki.org/wiki/Freedoom) will also work.

Finally, we load into the level. However, there's not much to see: just a hallway leading into a large dark room... with a single imp. What can we do with this? Well, as DOOM is in fact [a 2D game](https://doomwiki.org/wiki/Room-over-room), it supports automatically drawing a top-down [automap](https://doomwiki.org/wiki/Automap) of the level. If we take a look at this... We will see the flag simply written in unreachable rooms, just out of bounds of the entrance hallway. Challenge completed!
