#!/usr/bin/env python3

import socket
import arguments
import argparse
import arguments
from arguments import _ip_address, _port, ArgumentTypeError

# Run 'python3 VPN.py --help' to see what these lines do
parser = argparse.ArgumentParser('Send a message to a server at the given address and prints the response')
parser.add_argument('--VPN_IP', help='IP address at which to host the VPN', **arguments.ip_addr_arg)
parser.add_argument('--VPN_port', help='Port number at which to host the VPN', **arguments.vpn_port_arg)
args = parser.parse_args()

VPN_IP = args.VPN_IP  # Address to listen on
VPN_PORT = args.VPN_port  # Port to listen on (non-privileged ports are > 1023)

def parse_message(message):
    # Parse the application-layer header into the destination SERVER_IP, destination SERVER_PORT,
    # and message to forward to that destination
    try:
        SERVER_IP, SERVER_PORT, message = message.split('#', 2)
        return SERVER_IP, SERVER_PORT, message
    except ValueError:
        return "Invalid message format. Format must be: <server_IP>#<server_port>#<message>"

### INSTRUCTIONS ###
# The VPN, like the server, must listen for connections from the client on IP address
# VPN_IP and port VPN_port. Then, once a connection is established and a message recieved,
# the VPN must parse the message to obtain the server IP address and port, and, without
# disconnecting from the client, establish a connection with the server the same way the
# client does, send the message from the client to the server, and wait for a reply.
# Upon receiving a reply from the server, it must forward the reply along its connection
# to the client. Then the VPN is free to close both connections and exit.

# The VPN server must additionally print appropriate trace messages and send back to the
# client appropriate error messages.

print("VPN starting - listening for connections at IP", VPN_IP, "and port", VPN_PORT)
# Create a IPv4 TCP socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((VPN_IP, VPN_PORT))
    # Listen for client connections
    s.listen()
    conn, addr = s.accept()
    with conn:
        # Flag to indicate when to exit the loop
        exit = False
        print(f"Connection established with client at {addr}")
        while exit == False:
            data = conn.recv(1024).decode('utf-8')
            print(f"Received client message: {data}")
            print("Parsing message...")
            # Parse the message to obtain the server IP address and port number
            SERVER_IP, SERVER_PORT, message = parse_message(data)

            try:
                valid_ip = _ip_address(SERVER_IP)
                print(f"Destination IP address: {valid_ip}")
            except ArgumentTypeError as e:
                print(f"Invalid destination IP address: {SERVER_IP}")
                conn.sendall(bytes(f"Invalid destination IP address: {SERVER_IP}", 'utf-8'))
                continue

            try:
                valid_port = _port(SERVER_PORT)
                print(f"Destination port: {valid_port}")
            except ArgumentTypeError as e:
                print(f"Invalid destination port: {SERVER_PORT}")
                conn.sendall(bytes(f"Invalid destination port: {SERVER_PORT}", 'utf-8'))
                continue

            print(f"Forwarding message to server at IP {valid_ip} and port {valid_port}")
            # Create a new socket to connect to the server
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_s:
                # Connect to the server
                server_s.connect((valid_ip, valid_port))
                print(f"Connection established with server")
                while True:
                    # Send the message to the server
                    server_s.sendall(message.encode('utf-8'))
                    print(f"Sending message '{message}' to server...")
                    # Wait for a reply from the server
                    reply = server_s.recv(1024)
                    if not reply:
                        print("No reply received from server, closing connection")
                        conn.close()
                        server_s.close()
                        exit = True
                        break
                    else:
                        print(f"Received reply from server: {reply.decode('utf-8')}")
                        print("Forwarding reply to client...")

                    # Forward the reply to the client
                    conn.sendall(reply)
                    print("Reply forwarded to client")
                    print("Forwarding complete, closing connection with server and client")
                    exit = True
                    break
