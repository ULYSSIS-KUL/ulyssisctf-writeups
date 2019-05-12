# mr-coffee writeup

The challenge can be solved by using netcat to connect to the HTCPCP server and sending a "start" message as described in RFC2324. A valid solution would be:

BREW /pot-1 HTTP/1.1
Content-Type: application/coffee-pot-command

start


The server isn't very strict giving you some options for alternate solutions:
- you can omit the Host: header, which is invalid for HTTP/1.1 but valid for HTTP/1.0
- the protocol name isn't checked, so HTTP/1.0, HTTP/1.1 and HTCPCP/1.0 are all valid
- both POST and BREW requests are accepted. This is compliant with the RFC
