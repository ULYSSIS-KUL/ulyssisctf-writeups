# framed writeup
Framed is a fairly simple stego challenge. On opening `painting.gif` for the first time, we see some flashing: this is a GIF animation, not a static image.

The logical next step is to look at the frames of this animation, using GIMP for example. This shows us each animation frame as a separate layer. The image contains four frames, one of which simply contains the flag.

## Notes
The painting used is [Marine met kielzog](https://www.muzee.be/nl/collectie-1/marine-met-kielzog) van Léon Spilliaert. The limited palette of GIF images does this painting a disservice, really.

This challenge was initially supposed to be somewhat harder: all delays were supposed to be zero, so that there would be no flashing and the image would just be drawn over eachother at the same time.

However, this ran into some issues: all modern browsers and image viewers impose a certain *minimum* delay on GIFs, [for historical reasons](https://www.biphelps.com/blog/The-Fastest-GIF-Does-Not-Exist). This makes this harder version of the challenge sadly impossible.
