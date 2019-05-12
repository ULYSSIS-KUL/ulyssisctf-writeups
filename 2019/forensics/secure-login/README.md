# secure-login

When searching the website there is nothing unusual. There is only a `Admin` button which redirects to `/admin.php`. This redirects us to a login screen. When trying different passwords, you'll notice that none of them work. So we have to try to find an exploit.

We open the developer tools of our browser and go to `/admin.php`. This will redirect us to the login screen with a 302 HTTP response code.
Maybe we can try to access the website with a client that doesn't listen to HTTP headers.

The solution is to download the website, `/admin.php`, via `curl` or alternatives. This will show you the flag.