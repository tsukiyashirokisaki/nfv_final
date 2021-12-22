import socket
import time
# bind_ip = "0.0.0.0"

def open_socket(counter):
  sockets = []
  for i in range(counter):
     s = socket.socket()
     print(i+3000)
     s.bind(('localhost', i+3000))
     s.listen(1)
     sockets.append(s)
  time.sleep(20)
open_socket(5)
# while True:
#     client,addr = server.accept()
#     print('Connected by ', addr)

#     while True:
#         data = client.recv(1024)
#         print("Client recv data : %s " % (data))

#         client.send("ACK!".encode())