# praamzius

> Yesterday, I asked a friend to help with a programming assignment, but
> the solution he gave me is... [not really helping](rot13.sh). Can you
> help me figure it out?

## The concept

This is 'simple' Python code, but obfuscated in various ways. It contains a
'bug' causing the flag not to be printed.

The first layer of obfuscation is a simple rot-13, using a bash dropper.
Changing `exec` into `print` reveals the 'real' source (with semicolons,
in Python!)

But that source isn't very straightforward. In fact, it's an interpreter
for a stack-based language à la Forth. The interpreted code is the huge
string in one of the first few lines.

Most of that code basically pushes the flag onto the stack (in reverse),
then iterates over these characters, and... drops them, then prints a
whitespace (the `v20.` at the very end). Removing the `v20` reveals the
flag. (In the original source, the `v20` is rendered as `i20`.)

Applying the necessary changes is very easy, but figuring out what to do
isn't as much.

