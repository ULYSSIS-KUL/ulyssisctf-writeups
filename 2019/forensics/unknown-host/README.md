# unknown-host

> I can't reach poeticcats.com, even though I know it's hosted on the address below. Now I'm missing out on all that nice cat-related poetry!

If we just visit the site in our web browser, we're presented with the default nginx screen. If we try to visit `poeticcats.com`, we notice that this website does not exist. The flavortext tells us that it should be hosted somewhere on the same server.

The reason we get the default nginx welcome page, is because a `server_name` was set in the nginx config. This configuration makes it possible to host multiple websites on one host. This means that you have to tell the web server you're looking for `poeticcats.com`. The easiest way to do this, is to add it to your [hosts file](https://en.wikipedia.org/wiki/Hosts_%28file%29). You can find it at the following location:

- Linux: `/etc/hosts`
- Windows: `%SystemRoot%\System32\drivers\etc\hosts`
- MacOS: `/etc/hosts` or `/private/etc/hosts`

When we try to visit the website again after having done this, we will indeed see the web page. In order not to mess up the pretty web page, the flag is printed in white. It can be easily found by using the find function of your browser to look for `FLG`, selecting the text or looking at the page source.
