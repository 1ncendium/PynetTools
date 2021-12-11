# netcat.py
# For when you do not have access to the netcat module on your system, and have no means to install it
# Part of the PynetTools repository, https://github.com/1ncendium/PynetTools
# Author: Incendium
# Github: https://github.com/1ncendium

import argparse
import socket
import shlex
import subprocess
import sys
import textwrap
import threading

def execute(cmd):
    """ execute takes a command, cmd, runs it and sends - 
        the output back to the client
    """
    cmd = cmd.strip()
    if not cmd:
        return
    output = subprocess.check_output(shlex.split(cmd),
                                     stderr=subprocess.STDOUT)
    return output.decode()

class NetCat:
    """ Here we create the NetCat object that will handle all of -
        The functions below.
    """
    def __init__(self, args, buffer=None):
        """ This functions defines we default values of the below parameters
        """
        self.args = args
        self.buffer = buffer
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    def run(self):
        """ The run function will call the listen function if we choose to-
            setup a listener. Otherwise, we call the send function
        """
        if self.args.listen:
            self.listen()
        else:
            self.send()

    def send(self):
        """ Here we create the send function, which again takes the self -
            argument. 
        """
        # Connect to the target and port
        self.socket.connect((self.args.target, self.args.port))
        print(f"succesfully connected to {self.args.target} on port {self.args.port}")
        if self.buffer:
            self.socket.send(self.buffer)

        # Setup a try/catch block so we can manually close the connection with CTRL-C
        try:
            # Create a loop to receive data from the target
            while True:
                recv_len = 1
                response = ''
                while recv_len:
                    data = self.socket.recv(4096)
                    recv_len = len(data)
                    response += data.decode()
                    # If there is no more data, we break out of the loop
                    if recv_len < 4096:
                        break
                # Otherwise, we print the response data and pause to get interactive input,
                # send that input, and continue the loop.
                if response:
                    print(response)
                    buffer = str(input(''))
                    buffer += '\n'
                    self.socket.send(buffer.encode())
        except KeyboardInterrupt:
            print('User terminated.')
            self.socket.close()
            sys.exit()

    def listen(self):
        """When we need to setup a listener, we call this function
            Arg is self.
        """
        # bind to target + port
        self.socket.bind((self.args.target, self.args.port))
        # listen with the maximum back-log of 5
        self.socket.listen(5)
        
        # start to listen in a loop
        print(f"Listening on {self.args.target}:{self.args.port}...")
        while True:
            try:
                client_socket, _ = self.socket.accept()
                print(f"Succesfully connected to {self.args.target} on port {self.args.port}")
                # pass connected socket to the handle method
                client_thread = threading.Thread(
                    target=self.handle, args=(client_socket,)
                )
                client_thread.start()
            # If we manually close the listener with CRTL-C, we close the socket and exit.
            except KeyboardInterrupt:
                print('Listener closed manually')
                self.socket.close()
                sys.exit()
    
    def handle(self, client_socket):
        """ The handle function will "handle" the logic to perform -
            file uploads, execute commands, and create an interactive shell.
            The program can perform these tasks, when operating as a listener.
        """

        # Setup execute argument
        if self.args.execute:
            # pass command to execute function
            output = execute(self.args.execute)
            # send output
            client_socket.send(output.encode())
            print(f'Succesfully executed command {self.args.execute}')
        
        # Setup upload argument
        elif self.args.upload:
            file_buffer = b''
            # setup a loop to listen for data coming in and add it to the buffer
            print(f"Waiting for write to {self.args.upload}")
            while True:
                client_socket.send(b'Please provide the content of the file')
                print("receiving")
                data = client_socket.recv(4096)
                print(f"the data is {data}")
                # If there is any data, add it to the file_buffer
                if data:
                    file_buffer += data
                else:
                    break
            # open the uploaded file as f and write file_buffer to it
            with open(self.args.upload, 'wb') as f:
                f.write(file_buffer)
            message = f'Saved file {self.args.upload}'
            # send the confirmation message
            client_sockets.send(message.encode())

        # Setup command argument
        elif self.args.command:
            cmd_buffer = b''
            # Setup loop to receive data and send response back
            while True:
                try:
                    # send a prompt to the sender
                    client_socket.send(b"BHP: #> ")
                    # wait for input
                    while '\n' not in cmd_buffer.decode():
                        # add received data to cmd_buffer
                        cmd_buffer += client_socket.recv(64)
                    response = execute(cmd_buffer.decode())
                    # if there is a response, encode it and send it
                    if response:
                        client_socket.send(response.encode())
                    cmd_buffer = b''
                # if there is a exception catch it as e and close the socket.
                except Exception as e:
                    print(f'server killed {e}')
                    self.socket.close()
                    sys.exit()

if __name__ == '__main__':
    """ Here we create the main block of our program.
        We define the arguments, and define how we want the program -
        to behave. Also, we give some examples of how to use the args.
    """

    parser = argparse.ArgumentParser(
        description='Personal Net Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(""" Example:
            netcat.py -t 192.168.1.108 -p 5555 -l -c # command shell
            netcat.py -t 192.168.1.108 -p 5555 -l -u=mytest.txt # upload to file
            netcat.py -t 192.168.1.108 -p 5555 -l -e \"cat /etc/passwd\" # execute command
            echo 'ABC' | ./netcat.py -t 192.168.1.108 -p 135 # echo text to server port 135
            netcat.py -t 192.168.1.108 -p 5555 # connect to server
            """ ))
    parser.add_argument('-c', '--command', action='store_true', help='command shell')
    parser.add_argument('-e', '--execute', help='execute specified command')
    parser.add_argument('-l', '--listen', action='store_true', help='listen')
    parser.add_argument('-p', '--port', type=int, default=5555, help='specified port')
    parser.add_argument('-t', '--target', default='192.168.1.203', help='specified IP')
    parser.add_argument('-u', '--upload', help='upload file')
    args = parser.parse_args()

    intro = """ 
    netcat.py by Incendium, inspired by Black Hat Python 2nd edition.
    Remember to use EOF (CTRL + D) when you are willing to read the output from commands and shell.
    """

    print(intro)

    if len(sys.argv[1:]) < 2:
        print("netcat.py [-h] [-c] [-e EXECUTE] [-l] [-p PORT] [-t TARGET] [-u UPLOAD]")
        print("")
        print(parser.epilog)
        sys.exit(0)

    if "-e" in sys.argv:
        print("remember this..")

    if args.listen:
        buffer = ''
    else:
        buffer = sys.stdin.read()

    nc = NetCat(args, buffer.encode())
    nc.run()