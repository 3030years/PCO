import socket
from threading import Thread
from datetime import datetime
from notifypy import Notify
import os

os.system("%s install notify.py" % input("pip command (normaly pip or pip3): "))

# server's IP address
# if the server is not on this machine,
# put the private (network) IP address (e.g 192.168.1.2)
SERVER_HOST = input("Server name: ")
SERVER_PORT = 5002  # server's port
separator_token = "<SEP>"
# we will use this to separate the client name & message

SERVER_PORT = int(input("Sever Port (default is 5002): "))


# initialize TCP socket
s = socket.socket()
print(f"[*] Connecting to {SERVER_HOST}:{SERVER_PORT}...")
# connect to the server
s.connect((SERVER_HOST, SERVER_PORT))
print("[+] Connected.")

# prompt the client for a name
name = input("Enter your name: ")


def listen_for_messages():
    lastmessage = ""
    notification = Notify()
    notification.application_name = "PyChat"
    notification.icon = ""
    while True:
        message = s.recv(1024).decode()
        print("\n" + message)
        if message != lastmessage:
            lastmessage = message
            notification.title = "New message: "
            notification.message = message
            notification.send()


# make a thread that listens for messages to this client & print them
t = Thread(target=listen_for_messages)
# make the thread daemon so it ends whenever the main thread ends
t.daemon = True
# start the thread
t.start()
while True:
    # input message we want to send to the server
    to_send = input()
    # a way to exit the program
    if to_send.lower() == 'q':
        print("Stopping Please wait and ignore code:")
        break
    # add the datetime, name & the color of the sender
    date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    to_send = f"""[{date_now}] {name}{separator_token}{to_send}"""
    # finally, send the message
    s.send(to_send.encode())

# close the socket
s.close()
