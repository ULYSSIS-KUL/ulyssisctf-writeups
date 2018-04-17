# Hiding in plain sight

> For this one you don't need any special server or network location to go to, you already have the solution. All you need to do is be quiet and listen to the echo.

## Write-up

"hiding-in-plain-sight" was probably the sneakiest challenge of this CTF. The flavor text could give you a hint:

> For this one you don't need any special server or network location to go to, you already have the solution. All you need to do is be quiet and listen to the echo.

It claims we already have the solution, that's strange. We need to be quiet and listen to the echo. After a little guesswork, and maybe getting introduced to [Wireshark](https://www.wireshark.org/) after solving the capture-the-zip challenge, we could find that the flag server was sending an UDP packet to port 7 (echo service) of every computer linked to the CTF network, once a minute. It contained the flag in plaintext.
