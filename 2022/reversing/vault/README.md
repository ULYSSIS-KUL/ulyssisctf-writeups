# vault
> Can you crack the code and open the vault?

## Write-up
### Initial observations
We are given a Java class file called `Vault.class`. When we executed the class file, we get the following prompt:
```
$ java Vault 
Enter code
```

Because this is a reversing challenge, we'll try to decompile the class file to figure out the code we need to enter. There's a lot of Java decompilers out there, we'll use `cfr`. The decompiled class file looks a bit like this:
```
public class Vault {
    private static char[] flag = new char[]{':', '3', 'h', '3', '6', '`', '1', '5', '5', 'b', 'm', 'c', '5', 'a', 'e', '=', 'e', 'l', '9', ':', '>', 'g', '?', 'b', '0', '9', '0', '0', '<', 'g', '8', 'm', 'e', '6', 'd', 'a', '6', '8', '6', '4', ';', '`', 'c', '0'};

    public static void main(String[] stringArray) {
        System.out.println("Enter code");
        String string = new Scanner(System.in).next();
        if (string.length() == 44) {
            string = string;
            if (Vault.bootstrap("220248737", 6, string.charAt(6)) != false) {
                ...
                System.out.print("FLG{");
                System.out.print(flag);
                System.out.println('}');
                return;
            }
        }
        System.out.println("Bad code");
    }

    ...
}
```

The class file contains a static field called `flag`, which seems to contain 44 characters. However, this field can't be the real flag, as it contains characters which aren't actually allowed in the flag (remember that flags are hexadecimal). Still, this field is probably related to the real flag.

The main method takes the input "code" and first ensures the length of the input is equal to 44. Then, for each code character position `n`, between 0 and 44, the following if statement is executed:
```
if (Vault.bootstrap("XXXXXXXXX", n, string.charAt(n)) != false) {
```

In other words, if the result of `bootstrap` for each character at `n` and magic string `XXXXXXXXX` is true, then the program outputs the `flag` field. This means that the `bootstrap` method must also modify the `flag` field.

Let's take a closer look at the `bootstrap` method:
```
    private static /* bridge */ /* synthetic */ CallSite bootstrap(Object object, Object object2, Object object3) {
        switch (Integer.parseInt((String)object2)) {
            case 191429130: {
                return new ConstantCallSite(cfr_ldc_0());
            }
            ...
        }
        return null;
    }
```

The `bootstrap` method takes 3 arguments: the magic string `XXXXXXXXX`, the code character position `n`, and the character `c` at that position. It then parses the magic string to a number and executes a switch statement. Interestingly, `bootstrap` returns a `CallSite` type. However, in the `main` method this return value was interpreted as a boolean?? This means something strange is going on...

When we look at the [Java documentation](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/invoke/CallSite.html) for a `CallSite` we see that it holds a `MethodHandle` target to be used by an `invokedynamic` instruction. `invokedynamic` is a special Java bytecode instruction which invokes a method dynamically (or indirectly) using a bootstrap method (in this case, the `bootstrap` method in `Vault.class`). This instruction does not have a Java language equivalent. As a result, many decompilers have issues with (or outright fail at) decompiling this instruction.

Let's now look at `cfr_ldc_0`:
```
    /*
     * Works around MethodHandle LDC.
     */
    static MethodHandle cfr_ldc_0() {
        try {
            return MethodHandles.lookup().findStatic(Vault.class, "transform232999354", MethodType.fromMethodDescriptorString("(IC)Z", null));
        }
        catch (NoSuchMethodException | IllegalAccessException except) {
            throw new IllegalArgumentException(except);
        }
    }
```

The `cfr_` prefix and comment tell us that this method is inserted by the `cfr` decompiler to work around "MethodHandle LDC". `ldc` is another Java bytecode instruction, which loads a specific constant from the Java ConstantPool. Feel free to Google this if you are interested, we won't need to think about the ConstantPool. In this case a `MethodHandle` constant is loaded by `ldc`. However, once again, this construct does not have a Java language equivalent. Therefore, `cfr` needs to insert a helper method.

Finally, let's look at the "transform" method called `transform232999354`:
```
    private static /* bridge */ /* synthetic */ boolean transform232999354(int n, char c) {
        if (c >= '0' && c <= '9' && c - 48 == 9) {
            int n2 = n;
            flag[n2] = c - 48 ^ flag[n2];
            return true;
        }
        return false;
    }
```

This method takes a character position `n` and the character `c`. Then, it makes sure `c` is a digit between 0 and 9. Finally, if `c - 48 == 9`, it sets the `flag[n]` character to the XOR of `c - 48` and the original character. In other words, if the  character is `'9'`: `flag[n] ^= 9` and the method returns true. This is probably the return value checked by the `main` method at the start.

### Obtaining the first character
If we go back to the `main` method, we can find the if statement for the first character:
```
if (Vault.bootstrap("350289789", 0, string.charAt(0)) != false) {
```

Now we can look at the `bootstrap` method to see which `MethodHandle` this magic string corresponds to:
```
            case 350289789: {
                return new ConstantCallSite(cfr_ldc_6());
            }
```
```
    /*
     * Works around MethodHandle LDC.
     */
    static MethodHandle cfr_ldc_6() {
        try {
            return MethodHandles.lookup().findStatic(Vault.class, "transform1596911488", MethodType.fromMethodDescriptorString("(IC)Z", null));
        }
        catch (NoSuchMethodException | IllegalAccessException except) {
            throw new IllegalArgumentException(except);
        }
    }
```

Finally, we find the implementation of the `transform1596911488` method:
```
    private static /* bridge */ /* synthetic */ boolean transform1596911488(int n, char c) {
        if (c >= '0' && c <= '9' && c - 48 == 9) {
            int n2 = n;
            flag[n2] = c - 48 ^ flag[n2];
            return true;
        }
        return false;
    }
```

Now we know that the first character of the code is supposed to be `'9'`. This means that the first character of the flag is equal to `':' ^ 9 = '3'`.

We could repeat this process manually for each of the 44 characters and obtain the flag. However, this is very time-consuming and there is a more interesting way to solve this. Instead, we can write a Java program using [ASM](https://asm.ow2.io/) to analyze the bytecode and find the code!

### Automating the solution
We will use the `asm` core and `asm-tree` API to analyze the bytecode of `Vault.class`. It might be useful to look through the `Vault.class` bytecode first using the `javap` tool. This allows us to easily read the bytecode and see where the interesting constants are defined.

In our main method, we will read the class file, set up some bookkeeping, and then loop through each of the methods in the class file:
```
    public static void main(String[] args) throws Exception {
        // No explanation necessary.
        ClassNode cn = new ClassNode();
        ClassReader cr = new ClassReader(Files.newInputStream(Paths.get("Vault.class")));
        cr.accept(cn, 0);

        String[] positionToMagic = new String[44];              // 44 code positions mapped to a magic string.
        Map<String, String> magicToTransform = new HashMap<>(); // magic strings mapped to a "transform" method.
        Map<String, Integer> transformToCode = new HashMap<>(); // "transform" methods mapped to the 0-9 code value.
        for (MethodNode mn : cn.methods) {
            // The main method contains all the information required to map code positions to magic strings.
            if (mn.name.equals("main")) {
                visitMain(mn, positionToMagic);
            }
            // The bootstrap method contains all the information required to map magic strings to "transform" methods.
            if (mn.name.equals("bootstrap")) {
                visitBootstrap(mn, magicToTransform);
            }
            // For each transform method, we can find the 0-9 code value inside that method.
            if (mn.name.startsWith("transform")) {
                visitTransform(mn, transformToCode);
            }
        }

        // When we found all the values, print each 0-9 code value!
        for (String magic : positionToMagic) {
            System.out.print(transformToCode.get(magicToTransform.get(magic)));
        }
        System.out.println("");
    }
```

Then, we will visit the `Vault.class` main method and extract all magic strings:
```
    private static void visitMain(MethodNode main, String[] positionToMagic) {
        AbstractInsnNode[] insns = main.instructions.toArray();
        for (int i = 0; i < insns.length; i++) {
            // From `javap`, we know that `ldc` of the position is 3 instructions before `invokedynamic`.
            if (insns[i] instanceof LdcInsnNode && i + 3 < insns.length && insns[i + 3] instanceof InvokeDynamicInsnNode) {
                int position = (int) ((LdcInsnNode) insns[i]).cst;
                // The `invokedynamic` name actually contains the magic string!
                // Note that this abuses the name field, normally this should contain the name of the target method.
                String magic = ((InvokeDynamicInsnNode) insns[i + 3]).name;
                positionToMagic[position] = magic;
            }
        }
    }
```

When we have the magic strings, we can map these strings to the "transform" methods:
```
    private static void visitBootstrap(MethodNode bootstrap, Map<String, String> magicToTransform) {
        AbstractInsnNode[] insns = bootstrap.instructions.toArray();
        for (int i = 0; i < insns.length; i++) {
            if (insns[i] instanceof LookupSwitchInsnNode) {
                List<Integer> keys = ((LookupSwitchInsnNode) insns[i]).keys;
                List<LabelNode> labels = ((LookupSwitchInsnNode) insns[i]).labels;
                for (int j = 0; j < labels.size(); j++) {
                    // From `javap`, we know that the `ldc` of the `MethodHandle` is 4 instructions after the label.
                    AbstractInsnNode ldc = labels.get(j).getNext().getNext().getNext().getNext();
                    Handle handle = (Handle) ((LdcInsnNode) ldc).cst;
                    // The `MethodHandle` name will be the right "transform" method name.
                    magicToTransform.put(keys.get(j).toString(), handle.getName());
                }
            }
        }
    }
```

Finally, for each "transform" method we can find the 0-9 code value:
```
    private static void visitTransform(MethodNode transform, Map<String, Integer> transformToCode) {
        AbstractInsnNode[] insns = transform.instructions.toArray();
        // From `javap`, we know that the code value is loaded in the 10th instruction.
        transformToCode.put(transform.name, ((IntInsnNode) insns[9]).operand);
    }
```

When we compile this Java file and execute it, we obtain the 44-digit code to pass to `Vault.class`!
```
$ javac -cp asm-9.2.jar:asm-tree-9.2.jar:. Solve.java
$ java -cp asm-9.2.jar:asm-tree-9.2.jar:. Solve
93976211448513193919647748138499360778719572
$ java Vault
Enter code
93976211448513193919647748138499360778719572
FLG{30a40b041fef4bd4fe838c8e41134c1df0df10152ed2}
```
