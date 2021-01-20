import socket
import select

HEADER_LENGTH = 128

HOST = '127.0.0.1'
PORT = 5000

# Creation du socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Liaison de l'IP et du Port
server_socket.bind((HOST, PORT))

# Limite de connexion à 10
server_socket.listen(10)

# Liste des sockets pour le select
sockets_list = [server_socket]

# Liste des clients
clients = {}

print(f'En attente de connexion sur {HOST}:{PORT}...')

# Traitement du message reçu
def receive_message(client_socket):

    try:

        # Recois le header qui contient la longueur du message
        message_header = client_socket.recv(HEADER_LENGTH)

        # Conversion du header en int
        message_length = int(message_header.decode('utf-8').strip())

        # Return le message avec le header et la data
        return {'header': message_header, 'data': client_socket.recv(message_length)}

    except:

        return False

while True:

    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

    for notified_socket in read_sockets:

        if notified_socket == server_socket:

            # Accepte une nouvelle connexion
            client_socket, client_address = server_socket.accept()

            # On recupere le pseudo du nouveau client
            user = receive_message(client_socket)

            # On ajoute le nouveau client dans la liste des socket
            sockets_list.append(client_socket)

            # On ajoute le nouveau client dans la liste des clients
            clients[client_socket] = user

            # Notification lorsqu'un client rejoint le chat
            print('{} a rejoint le salon'.format(user['data'].decode('utf-8')))

        else:

            # On récupère le message
            message = receive_message(notified_socket)

            # Notification lorsqu'un client quitte le chat
            if message is False:
                print('{} a quitté le salon'.format(clients[notified_socket]['data'].decode('utf-8')))

                # On retire le client de la liste des socket
                sockets_list.remove(notified_socket)

                # On retire le client de la liste des clients
                del clients[notified_socket]

                continue

            # Notification lors de l'envoi d'un message
            user = clients[notified_socket]
            print(f'{user["data"].decode("utf-8")} a envoyé: {message["data"].decode("utf-8")}')


