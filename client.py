# Python 3.12.3

import socket
import sys 
import time
import signal
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-ip', '--server_ip',
                    default="20.189.75.209", type=str, help="Sever IP Address")
parser.add_argument('-port', '--server_port', default=8080,
                    type=int, help="The port where service running on")
arguments = parser.parse_args()


def sigint_handler(signal, frame):
    print()
    print(PINK, 'Interrupted.')
    disconnect()
    print(GREEN, "Successfully Disconnected from the server!")
    sys.exit(0)


signal.signal(signal.SIGINT, sigint_handler)

# Colors
NORMAL = '\033[0m'
RED = '\033[31m'
GREEN = '\033[32m'
ORANGE = '\033[33m'
BLUE = '\033[34m'
PURPLE = '\033[35m'
YELLOW = '\033[93m'
PINK = '\033[95m'

__version__ = "DEV1.0.21"
print(NORMAL, f"Version: {__version__}")

HEADER = 64
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "DISC"
CONFIRM_CONNECTION_MESSAGE = "CONFIRM_CONNECTION!"
# Whatever IP address you found from running ifconfig in terminal.
SERVER = arguments.server_ip
PORT = arguments.server_port

ADDR = (SERVER, PORT)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def disconnect(action=DISCONNECT_MESSAGE):
    client.send(action.encode(FORMAT))

def send_msg(message: str, target: str, action="SEND"):
    action = action.encode(FORMAT)
    message = message.encode(FORMAT)
    # Target is the user whom you want to send to
    _target = target.encode(FORMAT)
    client.send(action)
    client.send(message)
    time.sleep(0.1)
    client.send(_target)
    status = int(client.recv(2).decode(FORMAT))
    if status == -1:  # Target Username Not Found
        print(RED, f"\nTarget Not Found. {target}: No such username.")
    if status == 0:  # Send Successfully
        return

def receive_msg(target="!ALL", action="RECV"):
    action = action.encode(FORMAT)
    client.send(action)
    NumberOfMessage = int(client.recv(256).decode(FORMAT)
                          )  # The number of messages
    messages_receive = []
    if NumberOfMessage == 0:
        pass
    else:
        for i in range(NumberOfMessage):
            message = str(client.recv(2048).decode(FORMAT))
            message_from = str(client.recv(2048).decode(FORMAT))
            messages_receive.append([message, message_from])
            return messages_receive

# Modes

# Both Send and Receive
def email_mode():
    while True:
        message_send = str(input(NORMAL + "Message: "))
        target = str(input(NORMAL + "Target: "))
        send_msg(message=message_send, target=target)
        time.sleep(0.25)
        messages_receive = receive_msg()
        if messages_receive == -1:  # Target Username Not Found
            print(RED, "Target Username Not Found")
            time.sleep(1)
            continue
        if messages_receive == None:
            print(YELLOW + "No message receive.")
        if messages_receive != None:
            for message, message_from in messages_receive:
                print(NORMAL, message_from + " 👉🏻 " + message)

# Receive Only
def receiving_mode():
    print(YELLOW, "Receiving...")
    while True:
        messages_receive = receive_msg()
        if messages_receive != None:
            for message, message_from in messages_receive:
                print(NORMAL, message_from + " 👉🏻 " + message)
        time.sleep(1)

# Send Only
def sending_mode(personal=True):
    print()
    if personal:
        target = input(f"{YELLOW}Which user do you want to personally chat with: ")
    while True:
        message_send = input(f"{NORMAL}Message: ")
        if personal == False:
            target = input(f"{NORMAL}Target: ")
        send_msg(message_send, target)
        time.sleep(1)

def confirm_connection():
    client.settimeout(3.0)
    try:
        confirm_message = client.recv(len(CONFIRM_CONNECTION_MESSAGE)).decode(FORMAT)
    except socket.timeout:
        return False
    if confirm_message == CONFIRM_CONNECTION_MESSAGE:
        return True
    if confirm_message != CONFIRM_CONNECTION_MESSAGE:
        return False

# Officially connecting to the server.
try:
    print(NORMAL, f"Server:{SERVER}, Port:{PORT}")
    client.connect(ADDR)
except:
    print(RED, "[ERROR] Cannot connect to the server.\nPlease check the server status or your network.\nIf you still can't connect to the server, please contact us with fanfansmilkyway@gmail.com")
    sys.exit()
else:
    if confirm_connection() == False:
        print(RED, "[ERROR] Cannot connect to the server.\nPlease check the server status or your network.\nIf you still can't connect to the server, please contact us with fanfansmilkyway@gmail.com")
        sys.exit()
    if confirm_connection() == True:
        print(GREEN, "[SERVER CONNECTED] Successfully connect to the server!")
        time.sleep(0.5)

# Ask username
username = str(input(NORMAL + "Type in your username: ")).encode(FORMAT)
client.send(username)

# Ask mode
print(YELLOW, "Welcome to Terminal Chatting. Choose the mode before you start:")
print(YELLOW, "1: Email Mode       2: Receiving Mode       3: Sending Mode")
print()
mode = input(f"{ORANGE} Type in which mode do you prefer?  ")

if mode == "1":
    email_mode()
if mode == "2":
    receiving_mode()
if mode == "3":
    print(YELLOW, "1.Personal Chat      2.Email Chat")
    send_mode = input(f"{ORANGE}Type in which sending mode do you prefer?  ")
    if send_mode == "1":
        sending_mode(personal=True)
    if send_mode == "2":
        sending_mode(personal=False)