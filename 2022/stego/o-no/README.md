# o-no writeup

You get a link like `http://127.0.66.1`, and when you go there, it redirects you to `http://127.0.66.1/hellο.php`. 
This page shows you a message, allegedly by the Greek mythological hero Odysseus, who tells you that he hid a flag for you. 
As a hint, the text points to the Greek alphabet. Another hint is in the challenge name, "o-no". A third pointer, a bit
more hidden, is when you copy the URL from your browser's address bar, and paste it somewhere: it will look like
`http://127.0.66.1/hell%CE%BF.php`.

All of those hints point at the fact that the "o" in `hellο.php` is not actually an "o",
but an omikron. This looks exactly like a Latin o but it is a different character.
To find the flag, replace the omikron with a Latin o in the URL.