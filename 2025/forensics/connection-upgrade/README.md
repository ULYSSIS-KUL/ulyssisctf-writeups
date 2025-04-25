# connection-upgrade writeup

The name `connection-upgrade` refers to the HTTP `Connection` header with `Upgrade` as value.
This is a hint that you'd have to establish a connection to a WebSocket server
(a request to a WebSocket server carries the `Connection: Upgrade` and `Upgrade: WebSocket` headers).

If you connected to `ws://<the IP>:8080`, the WebSocket server would send the flag every second.

There were several ways to connect to that server. One way is to download a tool like
[websocat](https://github.com/vi/websocat) to connect to the websocket. Another way, that didn't
require you to download anything, was to open your browser console and run a line of JavaScript code
that connects to the websocket and logs incoming messages:

```
let ws = new WebSocket("ws://127.0.66.1:8080/"); ws.onmessage = function(e) { console.log(e.data); }
```
