Build image

```shell
DOCKER_DEFAULT_PLATFORM=linux/amd64 docker build -t a901002666/k8s-udp-session-affanity .
```

Run image

```shell
docker run -it --rm a901002666/k8s-udp-session-affanity
```

Send udp pack
```shell
echo 'nino' | nc -4u -w1 localhost 10080
```



Test script

```python

import socket

UDP_PORT = 60002
UDP_IP = '127.0.0.1'
MESSAGE = 'ping'

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP, UDP_PORT))
```


echo 'nino' | nc -u -w1 104.199.252.119 10080
