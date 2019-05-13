#!/usr/bin/python3
import sys


def decode(code_in):
    flg_bin = "".join(["{:012b}".format(ord(i) - 0x2000) for i in code_in])
    return "{:044x}".format(int(flg_bin, 2))


try:
    cypher = sys.argv[1]
except IndexError:
    print("Please pass a cypher as input.")
    raise TypeError
else:
    print(decode(cypher))
