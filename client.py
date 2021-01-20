import socket, sys


HEADER_LENGTH = 128

HOST = '127.0.0.1'
PORT = 5000
pseudo = input("Username: ")

# Creation du socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Liaison de l'IP et du Port
client_socket.connect((HOST, PORT))

# Encode et envois le pseudo sur le serveur
username = pseudo.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(username_header + username)

# Message de bienvenue
print(f"Bienvenue à toi aventurier {pseudo}")

while True:

    # En attente d'un message
    message = input(f'{pseudo} > ')

    if message:

        # Encode le message et l'envois sur le serveur
        message = message.encode('utf-8')
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(message_header + message)
