#!/usr/bin/env python
import argparse
import sys
import socket
from library import CTFDict, Colors, loadAnimation, ASCII_ART, METADR, LOCALHOST
from threading import Thread
from time import sleep
import netifaces as ni


class ClientThread(Thread):
    def __init__(self, client_socket, ip, port):
        """[summary]

        Args:
            client_socket ([socket]): [holds the client socket]
        """
        Thread.__init__(self)
        self.client_socket = client_socket
        self.client_ip = ip
        self.client_port = port

    def run(self):
        self.client_socket.sendall(ASCII_ART.encode())
        self.client_socket.sendall(CTFDict.CHALLENGE_1.encode())
        while True:
            try:
                self.client_socket.sendall(bytes(">>> ", "utf-8"))
                answer = self.client_socket.recv(1024).decode().strip()
                if answer == str(CTFDict.SOLUTION_1):
                    self.client_socket.sendall(CTFDict.WON.encode())
                    self.closeConn()
                    return
            except BrokenPipeError:
                self.closeConn()
                return

    def closeConn(self):
        self.client_socket.close()
        print(f"{Colors.FAIL}[-] Client {self.client_ip}:{self.client_port} disconnected {Colors.ENDC}")


class Server():
    def __init__(self, address, port):
        """[summary]

        Args:
            address ([str]): [server's ip]
            port ([int]): [server's port]
        """
        self.initConn(address, port)

    @classmethod
    def initConn(self, address, port):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            server_socket.bind((address, port))
            server_socket.listen(5)
        except Exception:
            print("Could not bind address to port, use a different port or try again later")
            sys.exit()
        if args.verbose:
            print(f"{Colors.BOLD}Listening on {address} {port} ...{Colors.ENDC}")
        while True:
            try:
                (client_socket, (ip, port)) = server_socket.accept()
                print(f"{Colors.OKGREEN}[+] Connection established from {ip} at port {port} {Colors.ENDC}")
                client_thread = ClientThread(client_socket, ip, port)
                client_thread.daemon = True
                client_thread.start()
            except KeyboardInterrupt:
                print(f"\n{Colors.WARNING}We are shutting down the server {Colors.ENDC}")
                sleep(1)
                break
            except Exception as e:
                print(f"{Colors.FAIL}Error occured {e} {Colors.ENDC}")
                break


def verifyInter(ip):
    interfaces = ni.interfaces()
    for i in interfaces:
        # Checking if there's an ip assinged to the interface
        if len(ni.ifaddresses(i)) > 1:
            if ip == ni.ifaddresses(i)[2][0]['addr']:
                return True
    return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # Server settings args
    parser.add_argument('-p', '--port', metavar='', type=int, help='specify server\'s port', default=2802)
    parser.add_argument('-a', '--address', metavar='', type=str, help='specify server\'s address', default="0.0.0.0")
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-q', '--quit', action='store_true', help='quiet mode - default')
    group.add_argument('-v', '--verbose', action='store_true', help='verbose mode')
    args = parser.parse_args()
    if(verifyInter(args.address) or args.address == METADR or LOCALHOST):
        try:
            loadAnimation()
            if args.verbose:
                print(ASCII_ART)
            server = Server(args.address, args.port)
            sys.exit()
        except KeyboardInterrupt:
            sys.exit()
    print(f"{Colors.FAIL}Error occured. Try using a valid address or check network interfaces. {Colors.ENDC}")
