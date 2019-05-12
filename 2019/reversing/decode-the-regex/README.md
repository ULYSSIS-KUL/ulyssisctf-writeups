# Decode the regex

> A hacker locked us out of our own system. To tease us, he has provided us a PCRE regex that matches the password he set, but we don't know regex. Can you help us recover our system?
>
> `^FLG\{(?=d([d4f1b2a86ec39]){10}a(?1){15}a[^\WA-Z1246\s_]{16}\}$)(.)([4cn])\2(?=..3)(?=[138c]{5})(?=(?:(?!c).){3})[1c4][82c](.)(?!\d)\3\4\2(?!(.)\5)(?!89)[89]{2}.4(?=d.8.8)(?=.2.3).{5}4f(?=6d)(([6da])(?6)?\7)\g{-1}9[e57].\B[469]\2(?![a-z03589]).\g{-4}(?(1)a|b)8\2\4f(?=(.)\8)\d{2}(?<![037-9])(?!c)(?=[abcde]{3}\d{2})((?![bd]))[a-d](?9)[d-f](?9)[b-d](?!(?!03))[03]{2}\b`

We are greeted by a crazy regex. We immediately see that it starts with `FLG\{`, and also the flavortext hints that it matches the flag. Presumably, that's the only thing it matches.

The only way to solve this challenge is to analyse the regex part by part and try to figure out what it does. The flag format is too random to bruteforce, and generators that produce strings from regexes can't handle many of the PCRE features used in this regex.

* `^`: This is called an [anchor](https://www.regular-expressions.info/anchors.html). It is zero-width and matches the start of a string.
* `FLG\{`: Matches the literal string `FLG{`. This is the start of our flag.
* `(?=d([d4f1b2a86ec39]){10}a(?1){15}a[^\WA-Z1246\s_]{16}\}$)`: This is a [lookahead](https://www.regular-expressions.info/lookaround.html). It describes a pattern without moving the match position.
    * `d`: The first character is a literal: the flag starts with a `d`.
    * `([d4f1b2a86ec39]){10}`: A [character class](https://www.regular-expressions.info/charclass.html) is [repeated](https://www.regular-expressions.info/repeat.html) 10 times. This means that the 10 next characters are limited to a small subset. We already know that the flag format is hexadecimal, so this tells us that there are also no `0`, `5` or `7` on these positions. We also note that the character class is stored in [capturing group](https://www.regular-expressions.info/brackets.html) 1. We will get back to what capturing groups are, but for now you can just keep in mind that it is a way to store information.
    * `a`: This is again a literal character `a`, on the 12th position.
    * `(?1){15}`: This is what is called a [subroutine](https://www.regular-expressions.info/subroutine.html). Simply said, it matches the same pattern as captured in the first capturing group. So we know that characters 13 to 27 are also restricted to the same subset as characters 2 to 11.
    * `a`: Another literal `a` on position 28
    * `[^\WA-Z1246\s_]{16}`: This is again a character class, but it is negated. It matches everything *except* the characters listed in here. From the literals, we already know that there are no capital letters, numbers `1`, `2`, `4` and `6`, no underscore, and to `\W` or `\s`. `\W` is [shorthand](https://www.regular-expressions.info/shorthand.html) for `[^\w]`, which is again a negated character class, where `\w` is by itself a shorthand for `[A-Za-z0-9_]. So we exclude everything that's not alphanumeric. This character set holds for the next 16 characters.
    * `\}`: A literal `}, which means we are at the end of our flag.
    * `$`: This is again an anchor. It matches the end of the string. No character can be matched past this point.

So, this already gave is quite a lot information. We can fill in some parts of the string:

```
FLG{d..........a...............a................}
```

Some other information is also known, but does not directly translate to characters we can fill in. Up to the next parts!

* `(.)`: `(.)` creates a new capturing group. A [dot](https://www.regular-expressions.info/dot.html) in regex can match any character, so that doesn't directly give us any information. But we should note that the lookahead *did not move the match position*, so we are actually matching the `d` that we already know! We don't directly get a new character, but capturing group 2 is now aware that it matches a `d`.
* `([4cn])`: A simple character class. We know from the above that we can't match `n` at this position, but both `4` and `c` are possible matches. The result is stored in capturing group 3.
* `\2`: This syntax also refers to a previous capturing group. It is called a [backreference](https://www.regular-expressions.info/backref.html). In contrast to subroutines, backreferences match the exact same text as the capturing group did. So this doesn't match any character like the `.` did, but can only match a `d`.
* `(?=..3)(?=[138c]{5})(?=(?:(?!c).){3})[1c4][82c](.)(?!\d)\3\4\2`: While it may not be immediately obvious, this part defines the next 6 characters. Let's break it up again:
    * `(?=..3)`: Tells us that the third character (starting to count from the current match position) is a `3`.
    * `(?=[138c]{5})`: Tells us the next 5 characters are from this subset of 4 characters.
    * `(?=(?:(?!c).){3})`: This is a tough, but common, construct.
        * `(?!c)` is a negative lookahead, telling us the next character isn't a `c`. 
        * `(?:)` is syntax for a [non-capturing group](https://www.regular-expressions.info/brackets.html). We use it when we just want to group something, but not store it as a capturing group.
        * `(?:(?!c).){3}`: We simply repeat the pattern `(?!c).` three times, which means that the next three characters won't be a c. It is equivalent to `[^c]` in this case, but when using more interesting lookarounds, the construct definitely provides added value.
    * `[1c4][82c](.)(?!\d)\3\4\2`: This is just a list of characters we can fill in.
        * `[1c4]`: The second lookahead made the `4` impossible at this position, while the third lookahead disallows a `c` on this position. So this has to be a `1`.
        * `[82c]`: With the same reasoning, we can scratch the `2` and the `c` on this position, and we're left with the `8`.
        * `(.)`: The first lookahead tells us this has to be a `3`, which is captured by capturing group 4.
        * `(?!\d)\3`: `\3` refers back to the third capturing group, which we found was either a `4` or a `c`. The negative lookahead in front forbids numbers, so we can fill in a `c` on both positions.
        * `\4`: This refers back to the value matched by capturing group 4, which is a `3`.
        * `\2`: This is again a simple backreference, this time to the value in the second backreference, which is a `d`.

That was a lot to digest, so let's wrap up with an in-between flag status. Below the flag, the capturing groups are numbered for later reference.

```
FLG{dcd183c3d..a...............a................}
        23     4
```

* `(?!(.)\5)(?!89)[89]{2}`: Defines the next two characters.
    * `(?!(.)\5)`: We create the fifth capturing group and directly refer back to it. This is in a negative lookahead and means that the next two characters are not the same.
    * `(?!89)`: The next two characters are not literally `89`.
    * `[89]{2}`: The next two characters are `8` and `9`, in undefined order and occurrence. Since the last two lookaheads ruled out `88`, `99` and `89`, this has to be `98`.
* `.4`: The `.` can be any character, but after filling in 8 and 9 in the partial flag above, we see that it conveniently matches the `a` we already knew about. It is followed by a literal `4`.
* `(?=d.8.8)(?=.2.3).{5}`: The `.{5}` matches five characters, the two lookaheads in front define which ones they are.
    * `(?=d.8.8)`: The first, third and fifth characters are `d`, `8` and `8` respectively.
    * `(?=.2.3)`: The characters in between are literals `2` and `3`. Combined, we get `d2838`.
* `4f`: Again a simple literal `4f`.

Before we try to conquer the next few characters (probably the hardest part of the regex), we write down our current progress again.

```
FLG{dcd183c3d98a4d28384f.......a................}
```

* `(?=6d)(([6da])(?6)?\7)`
    * `(?=6d)`: We start of with two characters for free. The next two characters matched are a literal `6d`.`
    * `(([6da])(?6)?\7)`: Let's just break this up further... We do note at this point that the entire sequence is stored in capturing group 6.
        * `([6da])`: This is a simple character class that matches one of the three listed characters. The result is stored in capturing group 7.
        * `(?6)?`: We refer back to the pattern of capturing group 6. This is surprising, because we are still inside capturing group 6! We have made a recursive group. To make the recursion finite, matching `(?6)` at this point is [optional](https://www.regular-expressions.info/optional.html).
        * `\7`: This is a backreference to capturing group 7. The special thing here is that this character is recursively matched and changes at every recursion level.
    * Let's use an extra bullet point to put this all together. We are matching characters in pairs, with a recursive call in the middle. We don't know the recursion depth, but we know that every level gives us two extra characters. The first two are `6d`, so we can already fill in `6d(?6)?d6`. The only way to know when this recursion ends, is by counting characters. After we solved the rest of the regex, we know how many characters we still have to fill in. If you're good enough at regex, you can also just go over it and count the number of characters that are matched, that are not inside a lookaround. We count 20, with 24 spaces more to fill in, so the recursion stops after just one call. The entire string that is matched, is `6dd6`.
* `\g{-1}`: This construct is called a [relative backreference](https://www.regular-expressions.info/backrefrel.html). It refers back to the value of the previous capturing group. Since the recursive call stands on its own, this is a `6`. In case of doubt, this would be a good time to use a tool like [Regex101](https://regex101.com/) to check this assumption.
* `9`: After the last fight, we get a `9` for free.
* `[e57]`: This simple character class matches one of three characters. To know which one, we have to refer all the way back to the big lookahead at the beginning. We're still before the second `a`, so we can't match a `0`, `5` or `7` at this position. The `e` is the only possible value.
* `.`: Lines up nicely with the `a` we already know about.

Now we got to that point, let's recap again:

```
FLG{dcd183c3d98a4d28384f6dd669ea................}
```

* `\B`: This is a small extra, inserted solely to confuse you. `\b` (with a small b) is called a [word boundary](https://www.regular-expressions.info/wordboundaries.html). It matches in between a word-character and a non-word character. By itself, `\b` is zero-width. `\B` is the inverse: it matches everywhere `\b` does not. Since the flag is hexadecimal, it will always match and doesn't give us any extra information.
* `[469]`: If you have paid attention, you noticed we passed the second `a`. This means that we are now matching the other part of the big lookahead in the beginning, which forbids the numbers `4` and `6`. We match a `9` at this point.
* ` \2`: We refer back to the value of the second capturing group, which is a `d`.
* `(?![a-z03589]).`: We match one character that's not a letter, and not in `[03589]`. When we again combine this with the lookahead at the beginning, which forbids `[1246]`, we are left with `7` as only possible match.
* `\g{-4}`: We saw earlier that `\g{-1}` refers back to the last capturing group at this point, which would be the seventh. So `\g{-4}` refers back to 3 groups earlier, which is capturing group `4`. This is a `3`.
* `(?(1)a|b)`: Another new construct, this time a [conditional](https://www.regular-expressions.info/conditional.html). Since the first backreference was not optional, the condition evaluates to true and we will match an `a` here.
* `8\2\4f`: Another few literal characters. This matches `8d3f`.

We made some progress again, so time for a status update:

```
FLG{dcd183c3d98a4d28384f6dd669ea9d73a8d3f.......}
```

* `(?=(.)\8)\d{2}(?<![037-9])`: The middle part (and only part that consumes characters) matches two digits, the lookarounds at both sides match what these digits can be.
    * `(?=(.)\8)`: We create the 8th capturing group and directly refer to it. We match the same digit twice.
    * `(?<![037-9])`: The second digit (and by extension, the first) is not `[037-9]`, which we can again combine with the lookahead at the beginning, from which we get that `[1246]` are also disallowed. We are left with a `5`. Putting both together, we match `55`.
* `(?!c)(?=[abcde]{3}\d{2})((?![bd]))[a-d](?9)[d-f](?9)[b-d](?!(?!03))[03]{2}\b`: The last five characters are matched by a pretty long regex. Let's split it up again:
    * `(?!c)`: The first character is not a `c`.
    * `(?=[abcde]{3}\d{2})`: The first three characters are letters; we end with two digits.
    * `((?![bd]))`: The first character (keep in mind that we have only done zero-width matches!) is also not a `b` or a `d`. We store this in the 9th capturing group.
    * `[a-d]`: We finally get to match a character. Since we know that the first character is not a `c`, `b` or `d`, we are left with `a`.
    * `(?9)[d-f]`: Since `(?9)` refers back to the pattern or the 9th capturing group, we can substitue it with `(?![bd])`. We couldn't match `f` at this position either, so this must match `e`.
    * `(?9)[b-d]`: Again, the next character is not `b` or `d`. Since it has to be in the `[b-d]` range, we are left with only `c`.
    * `(?!(?!03))[03]{2}`: To finish this off, we are greeted by a nested negative lookahead. This is of course simply equivalent to `(?=03)`, which can also be matched by `[03]{2}`. We also note that this lines up nicely with the `\d{2}` from the earlier lookahead, but it didn't provide us with extra information in the end.
    * `\b`: A zero-width match of a word boundary. Not necessary, but it's a nice confirmation that we have indeed reached the `}` at the end.

We can now finish the entire flag:

```
FLG{dcd183c3d98a4d28384f6dd669ea9d73a8d3f55aec03}
```
