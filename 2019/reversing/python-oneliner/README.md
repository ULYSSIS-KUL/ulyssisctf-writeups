# python-oneliner writeup

The file decode.py shows the solution to this challenge. The encoding script does the following:

- calculates its own sha256 hash and takes the hexdigest (i.e. a string representing a hexadecimal number representing the hash)
- reverses this string (the first reduce() call)
- shifts the characters in the flag 1 ascii value up/down according to their index (even or odd index), except for the first one (the second reduce() call)
- XORs both strings together
- base64-encodes this value

Decoding is essentially the same process in reverse.
