# faulty-gps writeup
To solve this, you first need to convert the instructions to text by putting them into an online speech-to-text tool. Since many AIs can't do this without errors, the transcript has already been provided. Once you have this, you need to plot the instructions. Note: if the instruction is "left", you must turn left and also move forward one unit. Once you’ve plotted everything, the instructions will draw the flag.

With the handy `turtle` tool from python, the following code can draw the flag for us:
```python
from turtle import *
DISTANCE = 5

with open("instructions.txt") as file:
	for line in file:
		if "straight" in line:
			forward(DISTANCE)
		elif "left" in line:
			left(90)
			forward(DISTANCE)
		elif "right" in line:
			right(90)
			forward(DISTANCE)
		elif "around" in line:
			right(180)
			forward(DISTANCE)
```
