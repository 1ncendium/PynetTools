# TCP_proxy.py
# Need to quickly setup a TCP proxy for whatever reason? Here you go.
# Part of the PynetTools repository, https://github.com/1ncendium/PynetTools
# Author: Incendium
# Github: https://github.com/1ncendium

import sys
import socket
import threading

""" We create a HEX filter, which does the following:
    that when chr(i) == 3, we will provide the character
    ELSE we provide a dot (.)

    Also, this is a LC (list comprehension) with a range of 256:
        This LC will do the above for each i in the range of 0 to 255
"""
HEX_FILTER = ''.join(
    [(len(repr(chr(i))) == 3) and chr(i) or '.' for i in range(256)]
)

def hexdump(src, length=16, show=True):
    """ This hexdump function takes a string as src
        and will convert that string into an hexdump 
    """
    # If our src includes bytes, decode them first
    if isinstance(src, bytes):
        src = src.decode()
    
    # Create a empty list
    results = []
    # Take a piece of the src to dump and put it into the word variable
    for i in range(0, len(src), length):
        word = str(src[i:i+length])

        # We use the translate built-in function to substitute the string representation
        # of each character for the corresponding character in the raw
        # string (printable)
        printable = word.translate(HEX_FILTER)

        # Likewise we substitute the hex representation of the int value of every
        # character in the raw string (hexa)
        hexa = ' '.join([f'{ord(c):02X}' for c in word])
        hexwidth = length*3

        # We append the strings that contain the hex value of the index,
        # of the first byte in the word, the hex value of it
        # and its printable representation
        results.append(f'{i:04x} {hexa:<{hexwidth}} {printable}')
    if show:
        for line in results:
            print(line)
        else:
            return results

def receive_from(connection):
    """ This function handles all the incoming data from the connection
        It can be local and remote data.
    """
    # create empty buffer
    buffer = b""

    # default we set a five-second time-out
    # increase this time-out IF you're proxying traffic to other countries
    # or over lossy networks
    connection.settimeout(2)

    try:
        recv_len = 1
        # Setup a loop to read response data into the buffer
        while recv_len:
            data = connection.recv(4096)
            buffer += data
            recv_len = len(data)
            if recv_len < 4096:
                break
    except:
        pass
    # return buffer to caller (local / remote machine)
    return buffer

""" Sometimes you may want to modify the response or request packets
before the proxy sends them on their way

I created two functions (request_handler) and response_handler) to do just that
Inside these functions, you can modify the packet contents, perform
fuzzing tasks, test for authentication issues, or do whatever else your heart
desires. This can be useful, for example, if you find plaintext user credentials being sent and want to try to elevate privileges on an application by
passing in admin instead of your own username.
"""

def request_handler(buffer):
    # perform packet modifications
    return buffer

def response_handler(buffer):
    # perform packet modifications
    return buffer

def proxy_handler(client_socket, remote_host, remote_port, receive_first):
    """proxy_handler, like the name says, handles the data between the local and remote host
       The data that is received will be send to the hexdump function.
    """
    # Connect to remote host
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))
    
    # First, make sure we don't need to first initiate a connection
    # to the remote side and request data before going into the main loop
    # some servers to this (FTP servers for example will send a banner first)
    if receive_first:
        # receive data from remote socket
        remote_buffer = receive_from(remote_socket)
        # send buffer to hexdump 
        hexdump(remote_buffer)
    
        # Next up, we hand the output to the response_handler
        remote_buffer = response_handler(remote_buffer)
        if len(remote_buffer):
            print('[<==] Sending {} bytes to localhost.'.format(len(remote_buffer)))
            client_socket.send(remote_buffer)
    
    while True:
        """ Here the main loop starts where we continually read from the local client,
            process the data, and send it to the local client, read from the remote client,
            send it to the local client until we no longer detect any data
        """
        local_buffer = receive_from(client_socket)
        if len(local_buffer):
            print('[==>] Received {} bytes from localhost.'.format(len(local_buffer)))
            hexdump(local_buffer)
    
            local_buffer = request_handler(local_buffer)
    
            remote_socket.send(local_buffer)
            print('[==>] Sent to remote.')
    
        remote_buffer = receive_from(remote_socket)
    
        if len(remote_buffer):
            print('[<==] Received {} bytes from remote.'.format(len(remote_buffer)))
            hexdump(remote_buffer)
    
            remote_buffer = response_handler(remote_buffer)
            client_socket.send(remote_buffer)
    
            print('[<==] Sent to localhost.')

def server_loop(local_host, local_port,
                remote_host, remote_port, receive_first):
    """ The server_loop function will set up and manage the connection.
    """
    # Define the server socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Try to bind to the local_host + port
    try:
        server.bind((local_host, local_port))
    except Exception as e:
        print('Error on bind: %r' % e)

        print("[!!] Failed to listen on %s:%d" (local_host, local_port))
        print("[!!] Check for other listening sockets or correct permissions.")
        sys.exit(0)
    
    # If there was no error while binding to localhost we begin to listen
    print("[*] Listening on %s:%d " % (local_host, local_port))
    # Listen with a maximum back-log of 5 connections
    server.listen(5)
    
    # Start to wait for incoming connections
    while True:
        client_socket, addr = server.accept()
        # Print out the local connection information
        line = "[==>] Received incoming connection from %s:%d" % (addr[0], addr[1])
        print(line)

        # When a fresh connection request comes in, we hand it off to the
        # proxy_handler in a new thread which does
        # all of the send and receiving of bits
        proxy_thread = threading.Thread(
            target=proxy_handler,
            args=(client_socket, remote_host,
            remote_port, receive_first))
        proxy_thread.start()

def main():
    """ The main function will define the logic of how we want our proxy to operate.
        We define how to use the proxy, which arguments, and give examples.
    """
    # If there are not 5 arguments given while calling the TCP_proxy.py
    # We print out how to use the proxy + an example
    if len(sys.argv[1:]) != 5:
        print("Usage: ./proxy.py [localhost] [localport]", end='')
        print("[remotehost [remoteport] [receive_first]")
        print("Example: ./proxy.py 127.0.0.1 9000 10.12.132.1 9000 True")
        sys.exit(0)
    local_host = sys.argv[1]
    local_port = int(sys.argv[2])

    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])

    receive_first = sys.argv[5]

    # If the receive_first argument is True, we set receive_first to True,
    # Else receive_first = False
    if "True" in receive_first or "true" in receive_first:
        receive_first = True
    else:
        receive_first = False

    # Start the server loop to listen for connections
    server_loop(local_host, local_port,
        remote_host, remote_port, receive_first)
    
if __name__ == '__main__':
    main()