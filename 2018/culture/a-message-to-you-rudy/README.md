# A message to you, Rudy

> Dear rude(boy|girl|non-binary pal), the attached file contains code that should give you that flag you were looking for, but I don't know the language. People told me to use this one compiler - I forgot the name but it sounded icky - but I couldn't get it to work, so you're on your own here my fellow rude-person. GL and keep on skanking.

## Write-up

This challenge was quite simple: A C-INTERCAL file is provided, it has the flag hardcoded in it. C-INTERCAL's format for I/O however is, well uh, it sure is /something/ alright, so you can't easily read the flag from the source code. You can, however, just feed the file to a compiler and print it out. The file won't compile as is, however. After some googling, you will find that the code isn't polite enough, and after adding a few PLEASE statements, the file will compile and you get the flag. [Congratulations! You won!](https://www.youtube.com/watch?v=2KH2gc11XQU)

Anyway, here's <s>wonderwall</s> a bunch of INTERCAL fun facts:

- Trying to compile a file that has an extension other than '.i' will give you the following error:
<pre>ICL998I    EXCUSE ME,
                YOU MUST HAVE ME CONFUSED WITH SOME OTHER COMPILER
                CORRECT SOURCE AND RESUBNIT[sic]</pre>
- The original INTERCAL could only print out numbers, formatted as butchered roman numerals. 
- Eric S. Raymond's C-INTERCAL provides functionality to print out arbitrary strings. The format for this is described [here](http://catb.org/esr/intercal/ick.htm#C_002dINTERCAL-I_002fO), I'm not even gonna attempt to describe it (it took embarrasingly long for me to write a script to hardcode the flags into INTERCAL files).
  - ESR himself admits the format is quite hard to describe and that it's easier to just read the source code, which is located at [the intercal repo on ESR's gitlab, in the aptly named file cesspool.c](https://gitlab.com/esr/intercal/blob/master/src/cesspool.c#L502).
- Whenever you compile a C-INTERCAL file, there's a small chance that a random compiler bug is triggered, causing the resulting program to crash immediately when invoked, throwing the following error:
 <pre>E744 RANDOM COMPILER BUG</pre>
- INTERCAL is, obviously, an abbreviation for "COMPILER LANGUAGE WITH NO PRONOUNCEABLE ACRONYM"
- As hinted at above, ick refuses to compile files that are rude and don't say PLEASE often enough. If PLEASE is said too often, however, a file comes off as insincere, and ick will also refuse to compile the file.
