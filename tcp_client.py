# TCP_server.py
# Need to quickly setup a TCP_client for whatever reason? Here you go.
# Part of the PynetTools repository, https://github.com/1ncendium/PynetTools
# Author: Incendium
# Github: https://github.com/1ncendium

import socket

target_host = "0.0.0.0"
target_port = 9998

# create the socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect the client
client.connect((target_host,target_port))

# send some data
client.send(b"HELLO")

# receive some data
response = client.recv(4096)

# print the response
print(response.decode())

# close connection
client.close()
