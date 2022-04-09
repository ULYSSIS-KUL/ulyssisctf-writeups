# somatic writeup

The Wikipedia page, "Head", is a hint that the flag is hidden in a [HTTP header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers).
(A bit deceivingly, the flavortext and Wiki page could lead you into thinking that
the flag is hidden in the `<head>` or `<body>` HTML tags, but that's not the case.)

To find it, open the Network tab of your browser's web developer tools, load the
page, scroll up to the request of the `/` page, and check the HTTP headers of its
response.