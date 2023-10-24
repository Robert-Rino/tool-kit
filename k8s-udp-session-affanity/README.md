Test script

```python

import socket

UDP_PORT = 60002
UDP_IP = '127.0.0.1'
MESSAGE = 'ping'

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP, UDP_PORT))
```
