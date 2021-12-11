# TCP_server.py
# Need to quickly setup a TCP_client for whatever reason? Here you go.
# Part of the PynetTools repository, https://github.com/1ncendium/PynetTools
# Author: Incendium
# Github: https://github.com/1ncendium

import argparse
import socket
import sys
import textwrap

class Client:
    """ The Client class will handle the logic of our TCP_client,
        We create three functions.
        __init__, initialize the attributes of the class
        TCP_client, will create an socket and connect the client to it
        run, will run the TCP_client
    """
    def __init__(self, args):
        """ initialize the attributes of the class
        """
        self.args = args

    def TCP_client(self):
        """  TCP_client, will create an socket and connect the client to it
        """
        target_host = self.args.target
        target_port = self.args.port

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

    def run(self):
        """ run, will run the TCP_client
        """
        self.TCP_client()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
    description='Setup TCP client, by Incendium',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog=textwrap.dedent(""" Example:
        tcp_client.py -t 192.168.1.108 -p 5555
        """ ))
    parser.add_argument('-t', '--target', default='192.168.1.203', help='specified IP')
    parser.add_argument('-p', '--port', type=int, default=5555, help='specified port')
    args = parser.parse_args()

    tcpC = Client(args)
    tcpC.run()