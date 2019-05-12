The flag for this challenge is simply hidden somewhere encoded in UTF-8 binary representation.
In order to find the flag, given as "FLG{ ... }" we can look for the first few characters.
The binary representation of "FLG{" is 01000110 01001100 01000111 01111011 so now,
a search for this sequence quickly gives the location of the binary flag.
The final step is to decode the flag back into UTF-8 characters,
which can easily be done online or in a small script.
