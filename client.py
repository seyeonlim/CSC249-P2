#!/usr/bin/env python3

import socket
import arguments
import argparse

# Run 'python3 client.py --help' to see what these lines do
parser = argparse.ArgumentParser('Send a message to a server at the given address and print the response')
parser.add_argument('--server_IP', help='IP address at which the server is hosted', **arguments.ip_addr_arg)
parser.add_argument('--server_port', help='Port number at which the server is hosted', **arguments.server_port_arg)
parser.add_argument('--VPN_IP', help='IP address at which the VPN is hosted', **arguments.ip_addr_arg)
parser.add_argument('--VPN_port', help='Port number at which the VPN is hosted', **arguments.vpn_port_arg)
parser.add_argument('--message', default=['Hello, world'], nargs='+', help='The message to send to the server', metavar='MESSAGE')
args = parser.parse_args()

SERVER_IP = args.server_IP  # The server's IP address
SERVER_PORT = args.server_port  # The port used by the server
VPN_IP = args.VPN_IP  # The server's IP address
VPN_PORT = args.VPN_port  # The port used by the server
MSG = ' '.join(args.message) # The message to send to the server

def encode_message(message):
    # Add an application-layer header to the message that the VPN can use to forward it
    message = f"{SERVER_IP}#{SERVER_PORT}#{message}"
    return message

def run_client():
    print("client starting - connecting to VPN at IP", VPN_IP, "and port", VPN_PORT)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Connect to the VPN
        s.connect((VPN_IP, VPN_PORT))
        print(f"Connection established with VPN")
        talk_to_VPN(s)

def talk_to_VPN(sock):
    print(f"Sending message '{encode_message(MSG)}' to VPN...")
    # Send the message to the VPN
    sock.sendall(encode_message(MSG).encode("utf-8"))
    print("message sent, waiting for reply")
    # Wait for a reply from the VPN
    reply = sock.recv(1024)
    if not reply:
        print("Received empty input from VPN, closing connection")
        return False
    else:
        print(f"Received response from VPN: {reply.decode('utf-8')}")
        return reply

if __name__ == "__main__":
    run_client()
    print("Client is done, exiting...")
