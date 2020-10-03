#!/usr/bin/env python
import threading
import argparse
import socket
import sys
from vocab import dict, bcolors
from threading import Thread
from time import sleep


class ClientThread(Thread):
    def __init__(self, client_socket):
        Thread.__init__(self)
        self.client_socket = client_socket

    def run(self):
        self.client_socket.sendall(dict["WELCOME"].encode())
        self.client_socket.close()


class Server():
    def __init__(self, address, port):
        self.initConn(address, port)

    def initConn(self, address, port):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((address, port))
        if args.verbose:
            print(f"{bcolors.BOLD}Listening on {address} {port} ...{bcolors.ENDC}")
        server_socket.listen(5)
        while True:
            try:
                (client_socket, (ip, port)) = server_socket.accept()
                print(f"{bcolors.OKGREEN}[+] Connection established from {ip} at port {port} {bcolors.ENDC}")
                client_thread = ClientThread(client_socket)
                client_thread.daemon = True
                client_thread.start()
                client_thread.join()
            except KeyboardInterrupt:
                print(f"\n{bcolors.WARNING}We are shutting down the server {bcolors.ENDC}")
                sleep(1)
                break
            except Exception as e:
                print(f"{bcolors.FAIL}Error occured {e} {bcolors.ENDC}")
                break


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # Server settings args
    parser.add_argument('-p', '--port', metavar='', type=int, help='specify server\'s port', default=2802)
    parser.add_argument('-a', '--address', metavar='', type=str, help='specify server\'s address', default="0.0.0.0")
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-q', '--quit', action='store_true', help='quiet mode - default')
    group.add_argument('-v', '--verbose', action='store_true', help='verbose mode')
    args = parser.parse_args()
    server = Server(args.address, args.port)
