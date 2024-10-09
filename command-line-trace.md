# Client
% python3 client.py --server_IP 127.0.0.1 --server_port 65432 --VPN_IP 127.0.0.1 --VPN_port 65433 --message "add_days 2000-01-01 30"

client starting - connecting to VPN at IP 127.0.0.1 and port 65433

Connection established with VPN

Sending message '127.0.0.1#65432#add_days 2000-01-01 30' to VPN...

message sent, waiting for reply

Received response from VPN: The date after adding 30 days to 2000-01-01 is 2000-01-31.

Client is done, exiting...

# VPN
% python3 VPN.py --VPN_IP 127.0.0.1 --VPN_port 65433

VPN starting - listening for connections at IP 127.0.0.1 and port 65433

Connection established with client at ('127.0.0.1', 51008)

Received client message: 127.0.0.1#65432#add_days 2000-01-01 30

Parsing message...

Destination IP address: 127.0.0.1

Destination port: 65432

Forwarding message to server at IP 127.0.0.1 and port 65432

Connection established with server

Sending message 'add_days 2000-01-01 30' to server...

Received reply from server: The date after adding 30 days to 2000-01-01 is 2000-01-31.

Forwarding reply to client...

Reply forwarded to client

Forwarding complete, closing connection with server and client

# Server (example)
% python3 server.py --server_IP 127.0.0.1 --server_port 65432

server starting - listening for connections at IP 127.0.0.1 and port 65432

Connection established with ('127.0.0.1', 51009)

Received client message: add_days 2000-01-01 30

Parsing message...

Msg parsed and validity checked. Operation: add_days, Param1: 2000-01-01, Param2: 30

Operation: add_days, Param1: 2000-01-01, Param2: 30

Sending response to client...

Response sent to client!

Received empty input from client

Server is done!
