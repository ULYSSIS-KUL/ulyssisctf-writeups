# flaggle writeup

You are shown a clone of the Wordle game, but instead of guessing a word in 6 attempts, you have to guess the 44-character flag. Unlike in Wordle, there are no yellow cells marking a correct character at a wrong location. The cells are only filled with either green or gray.

The source code of the game reveals that a WebAssembly file is loaded, with the exported `check` function being loaded into `window.checkFlagDigits`:

```javascript
WebAssembly.compileStreaming(fetch("wasm/flaggle.wasm"))
    .then((module) => WebAssembly.instantiate(module, {}))
    .then((instance) => window.checkFlagDigits = instance.exports.check);
```

The rest of the source code seems to be mostly dealing with handling key presses. It also has three unused functions which may be helpful for you when trying out solutions: `inputAllAtOnce(s)` which takes a string and simulates an input for every character in the string, `clearAll()` which simulates 44 backspace presses, and `getCurrentRowAsString()` which concatenates all characters in the currently activated row into a string. There's also an obfuscated `enter` function with the following comment:

```javascript
// "enter" function, evaluates an attempted flag using checkFlagDigits by passing all characters of the flag from left to right one-by-one as numeric arguments, e.g. 6f8... would be checkFlagDigits(6, 15, 8, ...)
// perhaps the WebAssembly is easier to understand...
```

Because the usage of `checkFlagDigits` is obfuscated and the comment hints at inspecting the WebAssembly file, let's do just that. The [WebAssembly Binary Toolkit](https://github.com/WebAssembly/wabt) (WABT) has many useful tools about WebAssembly. The relevant tool in this instance is [wasm-decompile](https://webassembly.github.io/wabt/doc/wasm-decompile.1.html): "translate from the binary format to readable C-like syntax".

Decompiling the WebAssembly file, we see three functions: `select`, `check_digit`, and `check`. The latter is the exported function that's being called from JavaScript. There are also 24 bytes of read-only data in the assembly:

```
data rodata(offset: 1024) =
"G{\1d\0b\93\ae?\11z\88\f9\16M\18\84\14\81\bd\05\e3l\d1\9f\c4";
```

Since the flag is 44 hexadecimal characters long, it can fit in 22 bytes. This read-only data probably encodes the flag in some way.

Looking at the functions, it appears that the `check` function takes 44 arguments:

```c
export function check(a:int, b:int, c:int, d:int, e:int, f:int, g:int, h:int, i:int, j:int, k:int, l:int, m:int, n:int, o:int, p:int, q:int, r:int, s:int, t:int, u:int, v:int, w:int, x:int, y:int, z:int, aa:int, ba:int, ca:int, da:int, ea:int, fa:int, ga:int, ha:int, ia:int, ja:int, ka:int, la:int, ma:int, na:int, oa:int, pa:int, qa:int, ra:int):long
```

This matches the comment from the JavaScript file that the function is supposed to be called as `check(6, 15, ...)` and we know that the digits are passed from left to right. The bulk of the function body, after the assignments at the beginning, has a clearly repeated pattern, that looks like this (with some comments added about what's happening):

```c
var va:long = 0L;
ua[1]:long = va; // store va (0) on the stack (the stack pointer was set to ua at the beginning of the function)
var wa:long = ua[1]:long; // wa = va = 0
var xa:int = ua[47]:int; // ua[47] is a (the first function argument), as is clear from the assignments at the beginning of the function
var ya:int = 0;
var za:long = check_digit(wa, xa, ya); // check_digit(0, a, 0)
ua[1]:long = za; // store za (the result of check_digit) on the stack, replacing va
var ab:long = ua[1]:long; // ab = za
var bb:int = ua[46]:int; // ua[46] is b (the second function argument)
var cb:int = 1;
var db:long = check_digit(ab, bb, cb); // check_digit(za, b, 1)
ua[1]:long = db; // store db on the stack, replacing za
var eb:long = ua[1]:long; // eb = db
var fb:int = ua[45]:int; // ua[45] is c
var gb:int = 2;
var hb:long = check_digit(eb, fb, gb); // check_digit(db, c, 2)
...
return qh;
```

Most of the decompiled code shows variable assignments/renamings, so let's get rid of those and write some easier to read pseudocode:

```c
long result = 0;
result = check_digit(result, a, 0);
result = check_digit(result, b, 1);
result = check_digit(result, c, 2);
...
return result;
```

So the `check` function seems to be checking digits one-by-one and accumulating a result value. Let's take a look at the `check_digit` function:

```c
function check_digit(a:long, b:int, c:int):long {
  var d:int = stack_pointer;
  var e:int = 16;
  var f:{ a:int, b:int, c:long } = d - e;
  stack_pointer = f;
  f.c = a;
  f.b = b;
  f.a = c;
  var g:long = f.c;
  var h:int = f.b;
  var i:int = f.a;
  var j:int = select(i);
  var k:int = h;
  var l:int = j;
  var m:int = k == l;
  var n:int = 1;
  var o:int = m & n;
  var p:int = o;
  var q:long = i64_extend_i32_s(p);
  var r:int = f.a;
  var s:int = r;
  var t:long = i64_extend_i32_u(s);
  var u:long = q << t;
  var v:long = g | u;
  var w:int = 16;
  var x:int = f + w;
  stack_pointer = x;
  return v;
}
```

This would also be a lot more readable with less variable renamings. If we get rid of those, and remove the stack pointer operations, we get this pseudocode:

```c
function check_digit(a:long, b:int, c:int):long {
  int j = select(c);
  int m = b == j;
  int o = m & 1;
  long q = i64_extend_i32_s(o);
  long t = i64_extend_i32_u(c);
  long u = q << t;
  long v = a | u;

  return v;
}
```

That's much clearer. To simplify the above code further:

```c
function check_digit(a:long, b:int, c:int):long {
  long q = (long)((b == select(c)) & 1);
  
  return a | (q << c);
}
```

`q` will be `1` if `b` equals `select(c)`. Then `q` is left-shifted by `c` places, OR'd with `a`, and returned. We know from `check` that `a` is the accumulated result, `b` is the current digit, and `c` is the position of that digit (left-to-right, 0-based). From this we know that the accumulated result is a bit array, containing the equality check `b == select(c)` for each digit, and the least significant bit of the result is the equality check for the first digit.

But what is `select(c)`? In the context of the game, it needs to be checked which digits you guessed right or wrong. So it is logical that `select(c)` would return the correct digit at index `c`. Then if you guessed the flag entirely correct, the accumulated result at the end of `check` would be 44 `1` bits. Because the `select` function returns the correct digit at a given index, we can inspect what this function does, and derive all correct digits from it.

The decompiled `select` function looks like this:

```c
function select(a:int):int {
  var b:int = stack_pointer;
  var c:int = 16;
  var d:{ a:int, b:int, c:int, d:int } = b - c;
  d.d = a;
  var e:int = d.d;
  var f:int = 3;
  var g:int = e + f;
  d.c = g;
  var h:int = d.c;
  var i:int = 8;
  var j:int = h / i;
  var k:int = 1024;
  var l:int = 2;
  var m:int = j << l;
  var n:int_ptr = k + m;
  var o:int = n[0];
  d.b = o;
  var p:int = d.c;
  var q:int = 8;
  var r:int = p % q;
  var s:int = 2;
  var t:int = r << s;
  d.a = t;
  var u:int = d.b;
  var v:int = d.a;
  var w:int = u >> v;
  var x:int = 15;
  var y:int = w & x;
  return y;
}
```

We can perform a similar simplication of this function as for `check_digit`. Note that the `1024` refers to `data rodata(offset: 1024)`, and that left-shifting by two bits equals multiplying by 4.

```c
function select(a:int):int {
  int g = a + 3;
  int j = g / 8;  // integer division
  int r = g % 8;

  int o = *(&rodata + (j * 4));
  int w = o >> (r * 4);
  return w & 0xf;
}
```

Let's see what `select(0)`, the first digit of the flag, would return. `g` equals `3`, so `j = 0` and `r = 3`. This means that the first four bytes of the read-only data are stored in the integer `o`. These first four bytes are `0x47` (`G`), `0x7b` (`{`), `0x1d` and `0x0b`. Because WebAssembly uses little-endian encoding, `o` is `0x0b1d7b47`. Then `o` is right-shifted by `r * 4` bits. Because a hexadecimal digit consits of 4 bits, right-shifting by `r * 4` bits is the same as right-shifting by `r` hexadecmial digits. `r = 3`, so `w` becomes `0x0b1d7`. We only want to return the last digit, so `w & 0xf` is `0x7`. The first character of the flag is `7`.

We can find all digits by calculating `select(0)` up to `select(44)`, but we can get the flag faster by making the following observation. The digit is the least significant digit after right-shifting `o` by `r` hex digits, and when we take `select(1)`, we just shift one hex digit further to the right than for `select(0)`, giving us `d`. The first 5 characters of the flag are `7d1b0` by this reasoning, which looks like `0x0b1d7` in reverse! When taking `select(5)`, the sixth digit, `g` becomes 8 so `j = 1` and `r = 0`. `o` is `0x113fae93`. By reversing this again, we get the next 8 flag characters, `39eaf311`.

So, we can get flag characters by reversing hex digits of integers taken from `rodata`. Is there also an easy way to derive them directly from the string/bytes representation given by the decompilation process? Yes: because of the little-endian encoding, the order of the bytes in the hexadecimal integer representation is reversed compared to the string/bytes representation. This leads to the following procedure to easily extract the flag.

```
data rodata(offset: 1024) =
"G{\1d\0b\93\ae?\11z\88\f9\16M\18\84\14\81\bd\05\e3l\d1\9f\c4";
```

Get the hex value for every byte in this string:

```
47 7b 1d 0b 93 ae 3f 11 7a 88 f9 16 4d 18 84 14 81 bd 05 e3 6c d1 9f c4
```

Then, flip the hexadecimal digits of each byte:

```
74 b7 d1 b0 39 ea f3 11 a7 88 9f 61 d4 81 48 41 18 db 50 3e c6 1d f9 4c
```

Concatenate all digits, remove the first three (that's the effect of `a + 3` in `select`) and take the first 44 remaining digits (i.e. ignore the last one). Because `rodata` is 24 bytes/48 hex digits, it does contain 4 hex digits that are not part of the flag: the first three (explicitly skipped by `a + 3`) and the last one.

```
FLG{7d1b039eaf311a7889f61d481484118db503ec61df94}
```
