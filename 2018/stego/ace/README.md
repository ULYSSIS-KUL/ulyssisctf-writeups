# Ace

> "They provide the Paint for the Picture Perfect Masterpiece that You Will Paint on the Insides of Your Eyelids by the Bandits of the Acoustic Revolution" would have been a much more suitable title but it's too long for the scoreboard, so I put it in the description instead, besides Ace is pretty cool too (I assume you feel the same if you're after this flag, #pride I guess), but enough talk about actual cool stuff, here's some numbers to entertain yourself with.

## Write-up

This challenge was some basic stego. You were given a file (see ace.txt) which contains a bunch of lines that looked like this: 
<pre>#656565 121,40</pre>
In order to solve this challenge, you had to:
- figure out that the hashtag-followed-by-6-hexadecimal-digits thingy might very well be a color
- realize that there's exactly 60 000 lines in the file
- notice a couple of things about the two numbers separated by a comma:
  - see that the first one goes up to 600;
  - and that the second one goes up to 100;
  - multiply 600 by 100 and find it to be equal to 60 000, which just so happens to be the amount of lines in the file;
  - deduce that these numbers represent coordinates in a 600x100 grid
- conclude that each line denotes a 24-bit RGB pixel for a 600x100 image
- finally, find an image library for your favorite programming language and write a program to convert the file into an image
  - optionally, reconsidering which programming language is your favorite could save you some time

A sample solution in python is provided (see ace.py). For those interested, the 'source code' for this challenge is a <s>simple</s> one-liner (replace ace600x100.png with an image of your favorite flag):
<pre>convert ace600x100.png -fill black -gravity Center -annotate +0+10 "FLG{$FLAG}" txt:- | awk 'match($0, /([0-9]+,[0-9]+): \([0-9]+,[0-9]+,[0-9]+,[0-9]+\)  (#......)/, a) {printf "%s %s\n", a[2], a[1]}' | shuf > ace.txt</pre>

On a closing note, there's a rather queer joke in here, +1 street cred if you can figure it out.
