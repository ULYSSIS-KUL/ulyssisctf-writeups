# BaseEmoji

When opening the url, we are greeted with a encoded flag and a encoder.

when entering some text, we can see it's being encoded in emojis. 

If we only enter one or two characters, we can see that one `🚦` or two respectively show up at the end of the encoded text. This hints us at the `🚦` being a padding character.

We know we are dealing with a encoder. So it should be relatively easy to create a decoder, to decode the flag.

The name of the challenge `BaseEmoji` hints us to look at the `Base` types of encoding. After some searching, we can easily find that this type of encoding looks extremely like base64. The only thing we have to do is create the index table and decode the flag!