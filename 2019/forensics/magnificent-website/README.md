# magnificent-website writeup
The flag is hidden in a minified JavaScipt-file 'holder.js' in a function named 'secret'.
This is a simple static HTML-website. Thus, the flag has no real logic to hide itself. So, we start to search all the included files to find the flag. Since it is a given that a flag is surrounded by "FLG" and curly braces, we search on "FLG". We find the flag at last in the file "holder.js".
