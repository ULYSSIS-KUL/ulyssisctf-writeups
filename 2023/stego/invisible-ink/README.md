# invisible-ink writeup
In this challenge we are presented with a mysterious letter. Supposedly, our flag is written in "invisible ink" on the lower part of the page. We get the simple things out of the way first, the page is in fact pure white, there is no text written in #fffffe.

However, there are a few signs that the page is off. Normally, the text would be anti-aliased to appear nicer, but in this case it is not. However, it also does not have an appearance really matching a bitmap font, it is far too messy for this. The image has been posterized into using exactly two colors, black and white. Why could that be?

Furthermore, image viewers also think the image is a little weird. It is reported as "indexed 8-bit", rather than the more conventional "RGB 32-bit" or similar formats. `file`'s output is even more bizarre:
```
letter.png: PNG image data, 1050 x 1485, 2-bit colormap, non-interlaced
```
What even is a "2-bit colormap"?

The answer is that both "indexed" and "colormap" refer to what is more commonly known as a "palette". The pixels in this image do not specify a color directly. Instead, they specify an *index* into a *palette* of colors. This may be further confirmed by running `strings` on the file, which shows `PLTE`, the header for the PNG palette block, as one of the first strings.

But wait, this is a **2-bit** colormap? That means each index can use two bits, which means there are *four* palette colors. However, in the image, we only see two colors. Indeed, if we open the file in GIMP and open the "Colormap" interface, or use the dropper tool on locations until we find a pixel with index 2, we see that this image uses *three* palette colors. However, **two of these palette colors are identical**. Using the colormap interface, we can change the third palette color to a different color and reveal the flag. Challenge solved!
