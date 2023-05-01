# legacy writeup

The challenge gives you a file named `secret` that is clearly a non-text file. THe `file` command reveals the file type:

```
❯ file secret
secret: packed data, 112 characters originally
```

The "packed data", combined with the challenge's name, indicates that the file is compressed with the legacy Unix command [pack](https://en.wikipedia.org/wiki/Pack_%28compression%29) (*), from the 1980s. Although long obsolete, support to unpack files is still built into a modern Linux's `gzip`. Reading the contents of the file takes one simple command:

```
❯ zcat secret
A secret stored for future generations to find decades later.
FLG{970b0f0459b4a97827eb50be83ad776b09e2011154ac}
```

(or `gunzip < secret`, `gzip -d < secret`)

(*) Thanks to this implementation in Haskell: https://github.com/koalaman/pack
