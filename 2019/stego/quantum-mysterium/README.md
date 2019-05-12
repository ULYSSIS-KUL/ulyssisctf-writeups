# quantum-mysterium: solution

This is a 'Chimera' WAV file that is interpreted differently by different
media players. This happens because there are multiple `data` chunks.

But first, let's refresh on how WAV files work:

WAV is a RIFF-based format, which has the following structure:

```c
struct chunk_hdr {
    char magic[4];
    uint32_t content_length;
};
struct chunk {
    struct chunk_hdr hdr;
    uint8_t data[hdr.content_length];
};

struct riff_file {
    struct chunk_hdr file_header { .magic = "RIFF" };
    char wav_magic[4] = "WAVE";

    struct chunk chunks[];

    EOF = (uint8_t*)&header + header.content_length;
};
```

Common chunks are:

* `fmt `: contains data about sample rate, number of channels, bit depth,
          wave type, etc.
* `data`: contains the actual waveform blob.

When there are multiple `data` chunks for only one `fmt `, some media players
(like VLC, SoX, ...) default to the first one, while FFmpeg-based ones (and
others) pick the last one. This way, a third chunk can be inserted in the
middle, where the flag (pronounced by good ol' `espeak` using the NATO
alphabet) resides.

This chunk can be isolated with a small script, but this takes too much effort.
Instead, playing back the WAV file as a raw file (with the correct samplerate,
number of channels, etc.) works just as well. Audacity can do this ("Raw
import"), but `aplay -traw` and `play -traw` (part of SoX) do this, too.

## credits

The 'chaff' tracks were taken from:

* [Winnerdemo by Metalvotze (NSFW)](https://youtu.be/vLRCHZxOUmI)
* [We, Robots by ASD](https://www.youtube.com/watch?v=Yu97nTjhp4g)

