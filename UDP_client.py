# TCP_server.py
# Need to quickly setup a UDP_client for whatever reason? Here you go.
# Part of the PynetTools repository, https://github.com/1ncendium/PynetTools
# Author: Incendium
# Github: https://github.com/1ncendium


import socket

target_host = "127.0.0.1" #localhost
target_port = 9998

# create a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # notice the _DGRAM for UDP

# send some data
client.sendto(b"AAABBBCCC", (target_host,target_port)) # also notice the difference here

# receive some data
data, addr = client.recvfrom(4096)

print(data.decode())
client.close()