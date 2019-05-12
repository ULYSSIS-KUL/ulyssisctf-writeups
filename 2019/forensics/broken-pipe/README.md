# broken-pipe writeup
In this challenge you're confronted with a massive stream of seemingly garbage data. Of course, you know the format of the flag: it starts with `FLG{`. So you 'only' have to search this massive data stream for that.

The data is obviously encoded in base64, so you have to decode that first, but it's a lot of data to decode. Luckily, most shells support a nice feature called a 'pipe', represented by the `|` character. This lets you redirect the output of one program to another.

* The `curl` program downloads a URL and outputs it on the terminal.
* `base64 -d` will decode base64.
* `grep` may be used to search large amounts of text.

So `curl [ip] | base64 -d | grep FLG{` will easily output every line containing `FLG{` and thus the rest of the flag.

