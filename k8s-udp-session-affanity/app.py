#!/usr/bin/python3
import socket
import os

def loop_on_socket(s):
  while True:
    d, addr = s.recvfrom(1500)
    print(d, addr)
    s.sendto("ECHO: ".encode('utf8')+d, addr)

if __name__ == "__main__":
   # Instead of setting HOST to "0.0.0.0",
   # we set HOST to the Load Balancer IP
   HOST = os.environ.get('HOST') or '0.0.0.0'
   PORT = os.environ.get('PORT') or 60002
   sock = socket.socket(type=socket.SocketKind.SOCK_DGRAM)
   sock.bind((HOST, PORT))
   loop_on_socket(sock)

# 198.51.100.2 is the load balancer's IP address
# You can also use the DNS name of the load balancer's IP address
