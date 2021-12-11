# TCP_server.py
# Need to quickly setup a TCP_server for whatever reason? Here you go.
# Part of the PynetTools repository, https://github.com/1ncendium/PynetTools
# Author: Incendium
# Github: https://github.com/1ncendium

import argparse
import socket
import sys
import textwrap
import threading

class Server:
    """ The Server class will handle the logic of our TCP_server,
        We create three functions.
        __init__, initialize the attributes of the class
        main, will create an socket and connect the client to it
            - Within main we create handle_client that will handle receiving data
        run, will run the TCP_client
    """
    def __init__(self, args):
        """ initialize the attributes of the class
        """
        self.args = args

    def run(self):
        """ run, will run the TCP_client
        """
        self.main()

    def main(self):
        IP = self.args.target
        PORT = self.args.port

        # Create the server socker
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # bind server
        server.bind((IP, PORT))

        # start listening
        server.listen(5)
        print(f"[*] Listening on {IP}:{PORT}")

        def handle_client(client_socket):
            """ Will handle incoming data and decode it,
                Also sends a acknowledgement to the client.
            """
            with client_socket as sock:
                request = sock.recv(1024)
                print(f'[*] Received: {request.decode("utf-8")}')
                sock.send(b'ACK')

        while True:
            """ Start loop for incoming requests,
                We then create a new thread object that points to our,
                handle_client function, and we pass it the client socket object as an argument.
            """
            client, address = server.accept()
            print(f'[*] Accepted connection from {address[0]}:{address[1]}')
            client_handler = threading.Thread(target=handle_client, args=(client,))
            client_handler.start()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
    description='Setup TCP server by Incendium',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog=textwrap.dedent(""" Example:
        tcp_server.py -t 192.168.1.108 -p 5555
        """ ))
    parser.add_argument('-t', '--target', default='192.168.1.203', help='specified IP')
    parser.add_argument('-p', '--port', type=int, default=5555, help='specified port')
    args = parser.parse_args()

    tcp_server = Server(args)
    tcp_server.run()