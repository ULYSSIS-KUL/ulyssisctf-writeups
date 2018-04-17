# Capture the zip

> Our target was stupid enough to reuse the password protecting his PC, so we got in. We found out he was hosting the secret information we're looking for locally, but we have trouble extracting it. Can you help us?

## Write-up

The challenge page let us download a pcap file. It can be found [here](network-capture.pcap). The file name already tells us it's a network capture, and [Wikipedia confirms this](https://en.wikipedia.org/wiki/Pcap). We can use Wireshark to open it.

There are a lot of packets in there, so a small hint where we can look, would be nice. The flavor text tells us our target was hosting the secret information locally, so when scrolling through the capture, the connections to `127.0.0.1` really stand out! If we right click one of the packets and choose "Follow TCP Stream", we can see the request that was made:

```
GET /secret/archive.zip HTTP/1.1
```

A secret file was downloaded. Interesting! Can we retrieve it? Yes, we can! Wireshark has an option to extract files from a capture. You can find it in the menu: `File > Export Objects > HTTP`. It lists about a dozen objects, but of course, the one called `archive.zip` of type `application/zip` is the interesting one. We can save it on our computer for closer inspection.

When we open it, we can see a file called `flag.txt`. That's nice! But it appears to be password protected... How can we find the password?

The flavor text gave us a hint here:

> Our target was stupid enough to reuse the password protecting his PC, so we got in.

Would our target also be stupid enough to reuse the password for the secret zip? Can we find a password somewhere?

Going back to Wireshark to inspect the TCP stream again, we find something interesting: the first attempt to download the zip resulted in a `401 Unauthorized` response. Since the download did happen (we found the zip file in the pcap), this means that authentication has happened somewhere. It turns out that this was [HTTP Basic Auth](https://en.wikipedia.org/wiki/Basic_access_authentication), which we can see in the `Authorization` header:

```
Authorization: Basic YWRtaW46TTBzdFN1cDNyUzNjcjN0UEBzc3cwcmQzdjNy
```

This does not appear to be the password. The HTTP Basic Auth Wikipedia page tells us that a basic auth string is base64 encoded. Let's try that:

```
$ echo -ne "YWRtaW46TTBzdFN1cDNyUzNjcjN0UEBzc3cwcmQzdjNy" | base64 -d
admin:M0stSup3rS3cr3tP@ssw0rd3v3r
```

Gotcha! The password of the zip is `M0stSup3rS3cr3tP@ssw0rd3v3r`, and we can find the flag: `FLG{8syF7wRBv4YWcyJ9S9XFr1XGBMgMEZKwfhyMTzujzYub}`.
