#!/usr/bin/env python3

def fibonacci(i: int, previous: int = 1, past_previous: int = 0) -> int:
    for _ in range(i):
        previous, past_previous = previous + past_previous, previous
    return previous + past_previous

def rotate(character: str, n: int) -> str:
     return chr((ord(character) - 32 + n) % 95 + 32)

def encrypt(string: str) -> str:
    array = list()
    for index,char in enumerate(string):
        array.append(rotate(char, fibonacci(index)))
    return "".join(array)

import sys

to_encrypt = None
if len(sys.argv) < 2:
    to_encrypt = input("enter input: ")
else:
    to_encrypt = sys.argv[1]

print(encrypt(to_encrypt))
