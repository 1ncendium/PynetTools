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
*
- TCP_proxy
- netcat

## Prerequisites
Before you begin, ensure you have met the following requirements:

- Python 3.6+

## Downloading the tools

Linux :
```
git clone https://github.com/1ncendium/Quick-OS-Info.git
```
Windows :
```
Download the repository from https://github.com/1ncendium/Quick-OS-Info/archive/main.zip
```

## Using PynetTools

Linux :
```
chmod +x quickosinfo.py
```
```
python3 quickosinfo.py
```
Windows (Interactive mode) :
```
right click on quick_os_info_interactive -> "Run with PowerShell"
```
Windows :
```
Start PowerShell -> cd to QuickOS Info directory -> ./quick_os_info.ps1
```
