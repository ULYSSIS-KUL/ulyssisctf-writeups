The hexadecimal part of the flag (inside the brackets) is hidden in the unicode code points of utf-8 characters.
The cypher groups the hexadecimal numbers in sets three, starting from the least significant number (the end).
To each group it adds 0x2000 (hexidecimal number for 2*16^4) resulting in a group of four hexidecimal numbers.
These were converted to one number (of sixteen bits in binary), which was used as a unicode code point.
The code points, which describe the character number, were then written as the  utf-8 characters.
Your task is to decode the the utf-8 characters or the binary format to find the flag.

This challenge is fairly straightforward to solve.
A simple python script or even working with the binary format on paper suffice.
The main idea is to understand the algorithm and how UTF-8 encodes unicode code points.

A working solution can be found in the solution.py script.
Please ensure that you use the correct python version for utf-8.
All files are copyrighted ULYSSIS 2018-2019 and authored by Simon.
