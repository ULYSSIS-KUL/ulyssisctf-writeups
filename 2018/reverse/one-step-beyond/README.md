# One step beyond 

> Greetings,
>
> I've been watching you for a while and your work is quite interesting. I got one of those flags you're looking for. I'm not running a charity here though so you'll need to do me a favor. I managed to get a copy of the source code for this experimental military grade cryptography scheme that I want broken. I encrypted that flag you wanted with it. Reverse the crypto and you can decrypt your flag.
>
> Looking forward to see you handle this challenge.


## Write-up

This write-up explains how to de-obfuscate one-step-beyond.py. Note that it basicaly runs down the steps I took to obfuscate this code in reverse order, so this isn't a tutorial on how to de-obfuscate code. 

## Step one: exceptions are branches

The first thing to note here is that the code doesn't include any if-statements. However, there are a bunch of except clauses, making it reasonable to assume these except clauses handle the basic control flow rather than errors. You can print out the caught exceptions to see what the 'branch condition' for a given except clause is:

- t gives TypeError: object is not callable
- e gives IndexError: string index out of range
- f, r and d give ZeroDivisionError: division by zero

The code becomes clearer if we replace these by explicit branching. For the division by zero, it's quite easy to see these are triggered by the no-op statements i/i, n/n and m/((~z)&m) (there's no other division operations in these functions) which can be removed if we use explicit branching. 

In e there's also a no-op statement which triggers the IndexError. 

In the t function there's only one line which can trigger an error: r = r() will trigger an exception if r is not callable.

All these try-except blocks can be replaced by if-else blocks, as shown in if-statements.py

## Step two: figuring out the t function

Looking at the program, you can see that f, r, d and e:

- are never called directly, but are instead passed as arguments to the t function
- return a lambda expression in one of their branches, a non-callable object in the other
  - these lambda expressions act as 'partial applications' of the function generating them
  
Now it's not hard to see what the t-function does: Provided with a function and a set of arguments, it calls that function, and then as long as it keeps returning those lambdas, it calls those lambdas. Those familiar with the nitty gritty implementation details behind functional programming languages may recognise this construction as a trampoline, which is a hack to allow tail-call optimisation in a language without native support for it. The functions f, r, d, and e can now be deduced to be tail-recursive functions. Rewriting them as such makes them easier to read, but do note that python doesn't support tail-call optimisation, so you will run into stack overflows if you do this (which is why we use a trampoline instead), and we'll be refactoring them out anyway (they're quite unpythonic). So just remember that

<pre>def factorial(n, acc = 1):
    if n == 0:
        return acc
    else:
        return factorial(n-1, n * acc)
factorial(5)</pre>
 
is equivalent to

<pre>def factorial(n, acc = 1):
    if n == 0:
        return acc
    else:
        return lambda: factorial(n-1, n * acc)
trampoline(factorial, 5)</pre>

## Step three: figuring out the recursive functions

tramp.py contains versions of these functions with the function and variable names de-obfuscated, in case you want some code to follow along.

### d

The d function dus a whole bunch of bit-twiddling on its two arguments. The experienced bit-wizard will recognise this as arithmetic substraction implemented in terms of bitwise operations. Further, note that the second argument has a default value of 3&5 which evaluates to 1, so that, when only provided with a single argument, the d function simply decreases it's argument by 1. It should not surprise you then to learn that, as a matter of fact, d stands for decrease. You can refactor this function away by simply inlining '-1' instead.

### r

Looking at the ord-chr-arithmetic mess in the lambda, you can see that c is a character which is being shifted over the range of 32 to 127 inclusive, which just so happens to be the range of printable ascii characters. It does this one step at a time during n recursive calls. As you may have figured, r stands for rotate, and this function does something similar to ROT-N (as in, ROT-13 but for an arbitrary number N). You can refactor all the recursive calls away by being a bit less dumb with the arithmetic here.

### f

This is the fibonacci function, a typical example of a function which can be elegantly expressed recursively (though this is incredibly inefficient without memoization, which is why we opted for a less elegant version). You can replace the recursive calls with a for-loop

### e

This is the encrypt function. It recurses over the input string (somewhat less elegantly than how one recurses over a string in haskell). It encrypts the Nth character by rotating it I times using the rotate function, where I is the Nth fibonacci number according to the fibonacci function. You can refactor the recursive calls away by just iterating over the input string.

## Rounding up

A final deobfuscated version of this idiocy can be found in final.py. Now that the 'encryption' algorithm has been de-obfuscated, it should be quite obvious how it can be reversed. If not, diffing sample-solution.py against one-step-beyond.py can be quite enlightening. 
