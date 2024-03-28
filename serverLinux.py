import socket
import threading
import os

host = "localhost"
port = 16000
server_address = host, port

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(server_address)
server.listen()

clients = []
usernames = []
admin = None

def broadcast(message, sender):
    for client in clients:
        if client != sender:
            client.send(message)

def leave(client):
    try:
        index = clients.index(client)
        clients.remove(client)
        username = usernames[index]
        usernames.remove(username)
        client.close()
        if client == admin:
            new_admin(client)
        broadcast(f'{username} has been removed from the chat'.encode('ascii'), client)
        print(f'{username} is no longer connect to the server')
    except ValueError:
        pass

def new_admin(client):
    global admin
    nl = '\n'
    if clients:
        admin = clients[0]
        admin_username = usernames[0]
        admin.send(f'{nl}You are now the admin. Use "KICK <username>" to kick a user or "END" to end the chat.'.encode('ascii'))
        broadcast(f'{admin_username} is now the admin.', client)

def handle(client):
    global admin
    while True:
        try:
            message = client.recv(1024)
            admin_username = usernames[0]
            new_message = message.decode('ascii')
            username, sep, message_str = new_message.partition(': ')

            if message_str.upper() == 'LEAVE':
                leave(client)
                break

            elif message_str.startswith('KICK ') and client == admin:
                target_username = message_str.split(' ')[1]
                kick_user(target_username)

            else:
                broadcast(message, client)

        except Exception as e:
            leave(client)
            pass
            break

def kick_user(target_username):
    if target_username in usernames:
        index = usernames.index(target_username)
        kicked_client = clients[index]
        leave(kicked_client)
    else:
        admin.send(f'User "{target_username}" not found.'.encode('ascii'))

def receive():
    while True:
        client, address = server.accept()
        print(f'Connected with {str(address)}')

        client.send('NICK'.encode('ascii'))
        username = client.recv(1024).decode('ascii')
        usernames.append(username)
        clients.append(client)

        print(f'username of the client is: {username}')
        client.send('Connected to the server'.encode('ascii'))
        client.send('To clear the console, press enter three (3) times'.encode('ascii'))
        broadcast(f'{username} has joined the chat'.encode('ascii'), client)

        if not admin: 
            new_admin(client)

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

os.system('clear')
print('Server is listening')
receive()
