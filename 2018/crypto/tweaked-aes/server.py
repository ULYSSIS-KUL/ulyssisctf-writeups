#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from binascii import hexlify, unhexlify
import os
import re

from Crypto.Cipher import AES

FLAG = 'FLG{{{}}}'.format(os.environ['FLAG'])
FLAG += '\0' * (-len(FLAG) % 16)
assert len(FLAG) % 16 == 0
CIPHER = AES.new(os.urandom(16))
TWEAK = os.urandom(16)

def xor(a, b):
    return bytes(a ^ b for a, b in zip(a, b))

def encrypt(tweak, msg):
    return CIPHER.encrypt(xor(tweak, CIPHER.encrypt(msg)))

def decrypt(tweak, msg):
    return CIPHER.decrypt(xor(tweak, CIPHER.decrypt(msg)))

ENC = b''.join(encrypt(TWEAK, FLAG[i:i+16]) for i in range(0, len(FLAG), 16))
VALID_STRING = re.compile(r'[0-9a-f]{32}')

def main():
    print('Tweak used:', hexlify(TWEAK).decode('utf-8'))
    print('Encrypted flag:', hexlify(ENC).decode('utf-8'))

    while True:
        try:
            command, *args = input('> ').split()

            if command == 'encrypt':
                tweak, msg = args
                if not (VALID_STRING.fullmatch(tweak) and VALID_STRING.fullmatch(msg)):
                    print('Invalid arguments to encrypt')
                    continue
                print('Encrypted message:', hexlify(encrypt(unhexlify(tweak), unhexlify(msg))).decode('utf-8'))

            elif command == 'decrypt':
                tweak, msg = args
                if not (VALID_STRING.fullmatch(tweak) and VALID_STRING.fullmatch(msg)):
                    print('Invalid arguments to decrypt')
                    continue
                if unhexlify(tweak) == TWEAK:
                    print('I\'m not going to decrypt the flag for you, sorry.')
                    continue
                print('Decrypted message:', hexlify(decrypt(unhexlify(tweak), unhexlify(msg))).decode('utf-8'))

            elif command == 'help':
                print('Available commands:')
                print('decrypt <tweak> <msg>: decrypt a block')
                print('encrypt <tweak> <msg>: encrypt a block')
                print('help: show this help text')
                print('quit|exit: leave')

            elif command in ('quit', 'exit'):
                print('Goodbye!')
                break

            else:
                print('Unknown command')

        except EOFError:
            break
        except ValueError as e:
            print('Parse error')

if __name__ == "__main__":
    main()
