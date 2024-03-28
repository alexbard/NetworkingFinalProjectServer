import socket
import threading
import os

username = input('Please enter your username: ')

while username == "":
    username = input('Username is empty, try again: ')

server_host = "18.226.214.246"
server_port = 42536
server_address = server_host, server_port

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(server_address)

def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(username.encode('ascii'))
            else:
                print(message)
        except:
            os.system('cls')
            print('You have been kicked from the chat')
            client.close()
            pass
            break

def write():
    while True:
        counter = 0
        words = input()

        while words == "":
            counter += 1
            words = input()
            if counter >= 2:
                os.system('cls')
                words = input()

        message = f'{username}: {words}'
        client.send(message.encode('ascii'))
        counter = 0

os.system('cls')

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()