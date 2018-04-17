# kushiro

> Hi, we retrieved an [executable from an old Windows 3.1
> system](kushiro.exe), but its contents seems to be
> garbled after all those years of bitrot. Can you make it
> readable for us?

## The concept

This isn't really an ancient executable, but rather a .NET binary.

Trying to run a decompiler on it results in... not very nice-to-read
code, because the binary is hand-written in MSIL, and
rare/undocumented instructions were used. Thus, one has to read the
disassembly. Looking up MSIL opcodes is *strongly* adviced.

On closer inspection, it seems to decrypt some binary data with
a keystream returned by a method called `FakeKeystream`...

Though, plugging in `RealKeystreamBecauseWeAreNiceEnoughToTellYou` crashes.

But we didn't lie! The keystream used is the *representation of the bytecode
of that method* as bytes.

This lesson in being evil ends here, though. [For now.](../hale/hale.md)

## Example code

```cs
// compile with a reference to kushiro.exe
using System;

// ...

byte[] GetPlain() {
    // keystream
    var k=typeof(Program).GetMethod(
            "RealKeystreamBecauseWeAreNiceEnoughToTellYou")
        .GetMethodBody().GetILAsByteArray();
    // ciphertext
    var c=Program.PID.BF;
    // plaintext
    var p=new byte[c.Length];

    for (int i = 0; i < c.Length; ++i) {
        p[i]=c[i]^k[i%kd.Length];
    }

    return p;
}
```

