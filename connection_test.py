# This Python scripy is used to test whether the client can connect to the server or not
import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_ip = '20.189.75.209'  # Replace with your server's IP
server_port = 8080

client_socket.connect((server_ip, server_port))
print("Connected to the server")
# Interact with the server