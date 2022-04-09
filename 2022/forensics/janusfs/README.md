# janusfs writeup

As the name may have suggested, this challenge is based on
https://github.com/NieDzejkob/cursedfs : the participants are given a
`janus.img` file that is both a FAT32 and an EXT2 image. When mounted as EXT2,
it contains a file called `a`, which is the first half of the flag, compressed
using gzip, to deter `strings`. The FAT32 image similarly contains a file `b`,
an xz-compressed (in LZMA mode) version of the second half of the flag.
