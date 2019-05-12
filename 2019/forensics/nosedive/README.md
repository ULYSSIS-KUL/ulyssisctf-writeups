# nosedive

This challenge is a ZX Spectrum tape archive encoded as a WAV file. when played
as a normal audio file, it sounds like harsh screeching (frequency-modulated
squarewave). Some might mistake it with [the sound of a dialup
modem](http://www.windytan.com/2012/11/the-sound-of-dialup-pictured.html), but
it's something entirely different!

The easiest way to get the flag is to run the WAV throught a wav2tap program,
and then to inspect that tape file using a hex editor, or loading it in an
emulator.

Several programs for doing the conversion:

* [tzxwav](https://github.com/shred/tzxtools) from tzxtools
* [audio2tape](http://fuse-emulator.sourceforge.net/) from fuse-emulator-utils
* [MakeTZX GUI](http://www.ramsoft.bbk.org.omegahg.com/maketzx.html) (Windows)

This challenge was inspired by [a ZX Spectrum-related easter egg in
Bandersnatch](https://twitter.com/gasmanic/status/1079164419488268288).

