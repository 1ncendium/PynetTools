# PynetTools
Some usefull network tools for when you do not have access to basic tools like netcat. You can also quickly setup a TCP server / client.

<img src="Images/snake.png">

## Tools included
### TCP_client
Quickly setup your TCP_client, you can fill in the data that you want to send to the server.
- Usage: python3 TCP_client.py [target] [port]
- Example: python3 TCP_client.py 192.168.101.8 5555

### UDP_client
Quickly setup your UDP_client, you can fill in the data that you want to send to the server.
- Usage: python3 UDP_client.py [target] [port]
- Example: python3 UDP_client.py 192.168.101.8 5555

### TCP_server
Quickly setup your TCP_server, this script starts a listener for incoming requests
- Usage: python3 TCP_server.py [target] [port]
- Example: python3 TCP_server.py 192.168.101.8 5555

### TCP_proxy
This tool will act like a proxy. This has many usefull examples like acting like a FTP server.
- Usage: python3 TCP_proxy.py [target] [port] [remote server] [remote port] [receive first]
- Example: python3 TCP_proxy.py 192.168.1.203 21 ftp.sun.ac.za 21 True.

[Receive first] must be True for FTP servers. Because most FTP servers first send a banner when connecting to it.

## Prerequisites
Before you begin, ensure you have met the following requirements:

- Python 3.6+

## Downloading the tools

Linux :
```
git clone https://github.com/1ncendium/PynetTools.git
```
Windows :
```
Download the repository from https://github.com/1ncendium/PynetTools/archive/refs/heads/main.zip
```
