# emojii-cryption write-up

We are given a bunch of emojis. They seem to change upon refresh. Some may be:

🍆🙌🙇🍻👤🐳🍢🐰🐷🌳😸🐴👤😱😱😳👥🍤👥👣🌴😹🥥🥡🥡🐶😲🌳😸👡👤😵🍦🍦😰🐰🥽
👆👌🙇🍻🍤🌳👢😰🌷😳🌸🌴🍤🐱🐱🌳🥥👤🥥🍣🐴🐹🥥👡🥡😶🌲🐳🌸🍡👤🌵👦🍦🐰🌰🥽
🙆👌👇👻🍤😳🥢😰😷🌳🐸😴🍤🐱🐱🌳🥥🍤👥👣🌴😹🥥👡🍡🐶🐲🌳🐸🥡🥤🌵🥦👦🌰😰🥽

Let's look closer at the first character in all of these. The code points for 🍆, 👆 and 🙆 are '0001f346', '0001f446' and '0001f646' respectively. They're different characters, so it is expected that the code points should be different, and given that they're all emoji, it's unsurprising that the '0001F' part is the same. So what's actually interesting about this, is that they all _end_ on '46'.

'46' is the (hexadecimal) ASCII value of 'F'. Similarly, we can find that the last byte of the emojis for the second spot all end on '4c', which is an 'L', and for the third byte they end on '47', which is a 'G'. We can use this to decode the rest of the flag: `FLG{d3b07384d113edec49eaa6238ad5ff00}`.

The double i in the challenge name was a subtle hint towards this challenge being simple ascii encoding hidden in emojis.
