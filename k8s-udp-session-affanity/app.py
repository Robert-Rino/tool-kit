# UDP echo server
import socket

HOST = "0.0.0.0"  # Standard loopback interface address (localhost)
PORT = 10080  # Port to listen on (non-privileged ports are > 1023)

s = socket.socket(socket.AF_INET , socket.SOCK_DGRAM)
s.bind((HOST, PORT))
print("Server started ...192.168.225..242:2222")
print("Waiting for Client response...")
while True:
       print(s.recvfrom(1024))


# # TCP echo server
# import socket

# HOST = "0.0.0.0"  # Standard loopback interface address (localhost)
# PORT = 1935  # Port to listen on (non-privileged ports are > 1023)

# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.bind((HOST, PORT))
#     s.listen()
#     conn, addr = s.accept()
#     with conn:
#         print(f"Connected by {addr}")
#         while True:
#             data = conn.recv(1024)
#             if not data:
#                 break
#             conn.sendall(data)
