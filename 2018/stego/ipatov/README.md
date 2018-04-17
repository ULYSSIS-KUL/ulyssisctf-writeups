# ipatov

> We have developped a product that can compress an executable file into
> another program! [We accidentally used it on an important piece of
> information](ipatov.exe), but we're having trouble extracting all the
> things. Can you help us?

## The concept

The executable given prompts for a password, and if it's correct, it displays
some ascii art.

The password can be retrieved using `strings -el` (`-el` for little-endian
UTF-16 strings, because Microsoft suffers from severe brain-damage).

When the zipfile is decrypted, another executable is revealed. This one
simply prints the ascii art. Upon closer inspection (i.e. running
`strings` on it again), the flag is revealed. It is used in a lonely
`File.Exists` call.

Another way of solving this, is by `strace`ing it when giving it the correct
password, as it will print the `(l)stat(2)` call from the `File.Exists`:

```
stat("FLG{...}", 0x7d5501eaf5d0) = -1 ENOENT (No such file or directory)
lstat("FLG{...}", 0x7d5501eaf5d0) = -1 ENOENT (No such file or directory)
```

I've seen this exact scheme being used in the wild to 'protect' some data that
has to be decrypted anyway. (Greets to Fairlight, even though it all fell
down. `:P`)

```
   ___   _______  ___ _ ________ ____________ ________ _______ _ _ ____________
  _\ /  /  / /> >_> /_\\\ ___  /\\  ___  / /\\\ ____  >\ ____ \\\\\\ ___/ __  /
 /  /  /  / / \_   /<___  \  \/\__  \  \/ /<__ <___ \/   >   \/  /  /  /  __\/
/  /__/  / <___/  //\___>  >/\ _ _>  >/  /\___>    >/   /       /  /  /  /
\_______/\_____> /<_______/<_////___//  /\________/<<<<<___/\  <<<<  <<<<
           pcy\__\                   \__\           \_______/   \__\  \__\
```

("Best viewed" with an Amiga font.)

## Example code

Binwalk can be used, but it doesn't correctly extract the zip in some way or
another, I forgot the details.

One can also use [dnSpy](https://github.com/0xd4d/dnSpy/releases) to decompile
and extract everything. It works out-of-the-box on Windows, but requires some
tweaking in order to get it to compile on Mono.

```cs
using System;
using System.Reflection;
using System.IO;

static class Program {
    static void Main() {
        var asm = Assembly.LoadFrom("ipatov.exe");

        byte[] data;
        using (var ms = new MemoryStream()) {
            // resource name can be found by using GetManifestResourceNames
            asm.GetManifestResourceStream("embedded.zip").CopyTo(ms);
            data = ms.ToByteArray();
        }

        File.WriteAllBytes("encrypted.zip", data);
        // now open encrypted.zip with your preferred program.
        // `unzip` on unixes doesn't seem to work, use 7-zip instead.
    }
}
```

