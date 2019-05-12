# The Conquest of Brain writeup

The challenge is won by reaching the end of the brainfuck program. The program asks for user input and then compares this to what is essentially a hardcoded string, going into an infinite loop if the input differs from the string.

## Basic walkthrough

If we let the program run until it first asks input, we can see a number of values are in the memory. These all correspond to ascii characters. The first three correspond to the string "ok " which is printed every time a correct character is read. The fourth value is an empty spot used for comparing the input to the next character. The following values correspond to the string "notTHeBEES!!" which is the password which needs to be entered (I was not very inspired at the time). 

## How it works

The brainfuck program is built up out of two basic building blocks and some glue code to print the "ok " strings.

This first "block" sets the first memory cell to the ascii value for 'o' (111). It loops 10 times (using cell 2 as a loop counter), and adds 11 to cell 1 inside the loop, ending at 110, and then adds 1 more outside the loop. All other characters are initialised similarly.

`
>++++++++++         # set cell 2 to 10
[
    <+++++++++++    # add 11 to cell 1
    >-              # subtract 1 from cell 2
]                   # loop back if cell 2 != 0
<+>                 # add 1 to cell 1
`

The second "block" compares reads a character as input and compares it to the cell next to it (which should be initialised with the ascii code for a character). It repeatedly subtracts 1 from both characters, until the first is 0. If the second is not equal to 0 by the end of the loop, the program will enter the infinite loop at the end of this snippet.

`
,                   # read input to cell 1
[
    -               # subtract 1 from cell 1
    >-              # subtract 1 from cell 2
    <
]                   # loop back if cell 1 != 0
>[]                 # infinite loop if cell 2 != 0
`

The entire code is essentially these two building blocks + some moving back and forth.
