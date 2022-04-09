# mendeleev
> Yesterday hackers breached our website and stole all our data! They didn't leave any trace except this gif, perhaps it's some sort of calling card?

## Write-up
When we open the `table.gif` file, we see a red square on what appears to be the periodic table, first discovered by Mendeleev. Unfortunately, the red square is moving very fast, so it's difficult to figure out what's happening. We can extract the gif frames using a number of tools, for example ImageMagick (but many online tools might also work):
```
$ convert -coalesce ./table.gif frame%05d.png
```

This gives us 23 different frames, with a red square marking some element on the table. If we look at a reference table (for example the one on [Wikipedia](https://upload.wikimedia.org/wikipedia/commons/4/4d/Periodic_table_large.svg)) matching the blank table in the gif, we see that the following elements are marked:
```
Ra Au Pb Ge Lv Rf Md Ge Es Rg Mt Mt Md Ds Lv Ge Ts Mc Db Ds Lr Ge Am
```

This looks like some kind of code. Apart from a name, each chemical element also has an atomic number:
```
88 79 82 32 116 104 101 32 99 111 109 109 101 110 116 32 117 115 105 110 103 32 95
```

This looks a lot like ASCII! When we decode the numbers, we get:
```
XOR the comment using _
```

Which comment could this refer to? The [Wikipedia page](https://en.wikipedia.org/wiki/GIF#Metadata) of GIF tells us the following:
```
Metadata can be stored in GIF files as a comment block, a plain text block, or an application-specific application extension block.
```

If we open the file using GIMP (or use a website to extract the metadata), we find the following comment:
```
\x19\x13\x18$:;m9goi:o:>9fm<imjm:m:ffmk<gi=;>:<gmifm<l=o:"
```

Using Python, we can decrypt the comment as follows:
```
>>> "".join(chr(ord(x)^ord('_')) for x in "\x19\x13\x18$:;m9goi:o:>9fm<imjm:m:ffmk<gi=;>:<gmifm<l=o:\"")
'FLG{ed2f806e0eaf92c6252e2e9924c86bdaec82692c3b0e}'

```
