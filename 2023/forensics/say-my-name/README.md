# say-my-name writeup

We are presented with a website with a perhaps familiar name and theming:

> This is Zombo.com, and Welcome! Anything is possible, here at Zombo.com!
> The only limit is... you didn't call me by my name.
>
> If you can call me by my name, I'll show you that anything is possible,
> here at Zombo.com!

But what does "calling" a website "by its name" mean?

Well, in the main CTF web UI, we were given an IP address to navigate to it,
not a domain name. Websites also register which domain name you are asking for,
by looking at the `Host:` header of the HTTP response.

To see how this happens, let's use `curl` with the `-v` flag to have it tell us
what exactly it is transmitting (assuming the IP address of the challenge is
`127.0.66.1`):

```
$ curl -v 127.0.66.1
*   Trying 127.0.66.1:80...
* Connected to 127.0.66.1 (127.0.66.1) port 80 (#0)
> GET / HTTP/1.1
> Host: 127.0.66.1
> User-Agent: curl/7.83.1
> Accept: */*
> 
* Mark bundle as not supporting multiuse
< HTTP/1.1 200 OK
< Server: nginx/1.18.0 (Ubuntu)
[...]
< Accept-Ranges: bytes
< 
<html>
	<head>
		<title>say-my-name</title>
[etc.]
```

As you can see, by default, `curl` (and presumably your browser, too) sends the
IP address as the `Host:` string, not a website name.

With the `-H` flag of `curl`, we can tell it to use a different value:

```
$ curl -H "Host: zombo.com" -v 127.0.66.1
*   Trying 127.0.66.1:80...
* Connected to 127.0.66.1 (127.0.66.1) port 80 (#0)
> GET / HTTP/1.1
> Host: zombo.com
> User-Agent: curl/7.83.1
> Accept: */*
> 
* Mark bundle as not supporting multiuse
< HTTP/1.1 200 OK
[...]
< Accept-Ranges: bytes
< 
<html>
	<head>
		<title>say-my-name</title>
		<style>
			html { color-scheme: light dark; }
			body { width: 35em; margin: 0 auto;
			font-family: Tahoma, Verdana, Arial, sans-serif; }
		</style>
	</head>
	<body>
		<div><img src="/Zombocom.png" alt="Zombo.com logo" /></div>
		<h1>Welcome to Zombo.com!</h1>
		<p>
			This is Zombo.com, and Welcome! Anything is possible, here at Zombo.com!
			The only limit is yourself!
		<p/>
		<p>
			And as you have surpassed yourself in this challenge, we will now
			demonstrate that indeed, at Zombo.com, anything is possible, even
			obtaining the flag!
		</p>
		<p>
			FLAG{5c026ecfd13931c41fc2701bba79dc55aefe60de1b61}
		</p>
		<p>
			This is Zombo.com, and welcome to you, who has come to Zombo.com.
		</p>
	</body>
</html>
```

And thus we are given the flag.

Another way of solving this, is to add the following line to `/etc/hosts`:

```
127.0.66.1	zombo.com
```

Then we can look up `zombo.com` in a browser, and it'll give us the flag as
well.
