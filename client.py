import socket
import sys
import time
import signal

def sigint_handler(signal, frame):
    print()
    print(PINK, 'Interrupted')
    disconnect()
    print(GREEN, "Successfully disconnected from the server.")
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

HEADER = 64
PORT = 8080
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "DISC"
# Whatever IP address you found from running ifconfig in terminal.
SERVER = "20.189.75.209"
#SERVER = "127.0.0.1"

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
    if status == -1: # Target Username Not Found
        print(RED, f"\nTarget Not Found. {target}: No such username.")
    if status == 0: # Send Successfully
        return

def receive_msg(action="RECV"):
    action = action.encode(FORMAT)
    client.send(action)
    NumberOfMessage = int(client.recv(256).decode(FORMAT))  # The number of messages
    print(NumberOfMessage)
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

def email_mode():
    while True:
            message_send = str(input(NORMAL + "Message: "))
            target = str(input(NORMAL + "Target: "))
            send_msg(message=message_send, target=target)
            time.sleep(0.25)
            messages_receive = receive_msg()
            if messages_receive == -1: # Target Username Not Found
                print(RED, "Target Username Not Found")
                time.sleep(1)
                continue
            print(messages_receive)
            if messages_receive == None:
                print(YELLOW + "No message receive.")
            if messages_receive != None:
                for message, message_from in messages_receive:
                    print(message_from + " 👉🏻 " + message)

def receiving_mode():
    try:
        while True:
            receive_msg()
            time.sleep(1)
    except:
        send_msg(message=DISCONNECT_MESSAGE, target="!SERVER")


# Officially connecting to the server.
try:
    client.connect(ADDR)
except:
    print(RED, "[ERROR] Cannot connect to the server.\nPlease check the server status or your network.\nIf you still can't connect to the server, please contact us with fanfansmilkyway@gmail.com")
    exit()
else:
    print(GREEN, "[SERVER CONNECTED] Successfully connect to the server!")
    time.sleep(0.5)

# Ask username
username = str(input(NORMAL + "Input your username: ")).encode(FORMAT)
client.send(username)

print(YELLOW, "Welcome to Terminal Chatting. Choose the mode before you start:")
print(YELLOW, "1: Email Mode       2: Receiving Mode")
print()
mode = input(f"{ORANGE} Type in which mode do you prefer?  ")

if mode == "1":
    email_mode()
if mode == "2":
    receiving_mode()