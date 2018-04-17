# Python bashing

> Do you know Python? Do you know Bash? Do you know _both_?

## Write-up

The goal of `python-bashing` should have been immediately clear from the description: create a program that is both valid Python *and* valid Bash, and make it print the same output. A valid solution would be uploading an empty file, but this won't work, and we see the following error message:

> Ah, you're mister smartypants, aren't you? I'm sorry to say that I have foreseen you submitting an empty file, or a file with just comments. You'll actually have to produce an output, so this trickery of yours does not work.

So you will have to actually solve the challenge instead. This is not an easy task by itself, but if you could find out these kind of programs are called "polyglots", the solution was actually [almost literally available on StackOverflow](https://stackoverflow.com/a/15190191).

We could adapt this script such that it prints the same string in both programming languages:

```
''''echo hello world
exit
'''

print('hello world')
```

Windows users could hit an extra obstacle here: a script with Windows line endings is not valid bash! Almost any text editor that is not notepad.exe is able to save a file with UNIX line endings though. When you have done that, the above program should work, and you will get the flag.
