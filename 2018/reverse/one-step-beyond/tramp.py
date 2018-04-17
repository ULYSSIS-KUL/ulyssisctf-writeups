#!/usr/bin/env python3

def trampoline(func, *args):
    result = func(*args)
    while callable(result):
        result = result()
    return result


def fibonacci(i: int, previous: int = 1, past_previous: int = 0) -> int:
    if i != 0:
        return lambda: fibonacci(trampoline(decrease, i), previous + past_previous, previous)
    else:
        return previous + past_previous


def rotate(character: str, n: int) -> str:
    if n != 0:
        n %= 95
        return lambda: rotate(chr((ord(character) - 31) % 95 + 32), trampoline(decrease, n))
    else:
        return character


def decrease(n: int, m: int = 1) -> int:
    if (~n)&m != 0:
        return lambda: decrease(n^m, ((~n)&m)<<1)
    else:
        return n^m


def encrypt(string: str, index: int = 0, array: list = []) -> str:
    if index < len(string):
        array.append(trampoline(rotate, string[index], trampoline(fibonacci, index)))
        return lambda: encrypt(string, trampoline(decrease, index, -1), array)
    else:
        return "".join(array)


import sys

to_encrypt = None
if len(sys.argv) < 2:
    to_encrypt = input("enter input: ")
else:
    to_encrypt = sys.argv[1]

print(trampoline(encrypt, to_encrypt))
