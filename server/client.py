#!/bin/python
import signal
import sys
import socket

daemon_quit = False

def quit_gracefully(signum, frame):
    global daemon_quit
    daemon_quit = True

def main():
    signal.signal(signal.SIGINT, quit_gracefully)
    serverHost = '127.0.0.1'
    serverPort = int(sys.argv[1])
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((serverHost, serverPort))

    file = open(sys.argv[2], "r")
    lines = file.readlines()
    file.close()
    for line in lines:
        line = str.encode(line.strip("\n"))
        client.send(line)
        data = client.recv(1024)
        data = data.decode("utf-8")
        sys.stdout.write(data)
        sys.stdout.flush()

    while not daemon_quit:
        data = client.recv(1024)
        if data:
            data = data.decode("utf-8")
            sys.stdout.write(data)
            sys.stdout.flush()

    client.close()

if __name__ == '__main__':
    main()