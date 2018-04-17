# cafebabe

> I've tried reading this file using JD-GUI, but it didn't work. Can you help me?

## Write-up

"This file" is a [Java class file](Cafebabe.class). The flavor text says that JD-GUI cannot decompile it, so we try another compiler. You can use cfr, procyon or even IntelliJ to read the file. We get the following code:

```java
/*
 * Decompiled with CFR 0_125.
 */
import java.io.PrintStream;

class Cafebabe {
    public static void main(String[] arrstring) {
        "FLG{" + '3' + 'H' + 'S' + 'z' + 'V' + 'o' + '3' + 'A' + '8' + 'y' + 'E' + 'A' + 'D' + 'o' + '5' + 'X' + 'V' + 'C' + 'f' + 'X' + 'u' + 'w' + 'b' + 'c' + 'n' + '1' + 'y' + 'f' + 'p' + 'J' + 'q' + 'G' + 'x' + 'v' + 'A' + 'E' + 'C' + '4' + 'e' + '5' + 'A' + 'u' + '5' + 'c' + '}';
        System.out.println("Hello World!");
    }
}
```

The flag is easily readable.
