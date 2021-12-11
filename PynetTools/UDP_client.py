# UDP_client.py
# Need to quickly setup a UDP_client for whatever reason? Here you go.
# Part of the PynetTools repository, https://github.com/1ncendium/PynetTools
# Author: Incendium
# Github: https://github.com/1ncendium

import argparse
import socket
import sys
import textwrap

class UDP:
    """ The Client class will handle the logic of our TCP_client,
        We create three functions.
        __init__, initialize the attributes of the class
        main, will create an socket and connect the client to it
        run, will run the TCP_client
    """
    def __init__(self, args):
        self.args = args

    def run(self):
        """ run, will run the TCP_client
        """
        self.main()

    def main(self):
        target_host = self.args.target
        target_port = self.args.port

        # create a socket object
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # send some data
        client.sendto(b"AAABBBCCC", (target_host,target_port))

        # receive some data
        data, addr = client.recvfrom(4096)

        print(data.decode())
        client.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
    description='Setup UDP client, by Incendium',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog=textwrap.dedent(""" Example:
        UDP_client.py -t 192.168.1.108 -p 5555
        """ ))
    parser.add_argument('-t', '--target', default='192.168.1.203', help='specified IP')
    parser.add_argument('-p', '--port', type=int, default=5555, help='specified port')
    args = parser.parse_args()

    udpC = UDP(args)
    udpC.run()
