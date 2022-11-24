import socket
import threading
from random import randint
import sys

host = '127.0.0.1'
port = 22000
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(2)
clients = []
aliases = []


def send_all_clients(message):
    for client in clients:
        client.send(message)


def handle_client(client):
    if client == clients[0]:
        client.send(b"Who do you want to play with? Please type <bot> or <player>: ")
        opponent = client.recv(1024).decode('utf-8')
        if opponent == "bot":
            client.send(b"How many rounds would you like to play?")
            scores = []
            number_of_rounds = int(client.recv(1024).decode('utf-8'))
            for rounds in range(0, number_of_rounds):
                guessed = False
                current_score = 1
                generated_number = randint(0, 50)
                print(generated_number)
                client.send(b"Give a number between 0 and 50, 0 and 50 included:")
                while guessed is False:
                    number = client.recv(1024).decode('utf-8')
                    print(number)
                    if int(number) == generated_number:
                        guessed = True
                        client.send(b"The number is correct!")
                        break
                    elif int(number) < generated_number:
                        client.send(b"The number you sent is lower than the number you have to guess...Guess again!")
                        current_score = current_score + 1
                    elif int(number) > generated_number:
                        client.send(b"The number you sent is higher then the number you have to guess...Guess again!")
                        current_score = current_score + 1
                scores.append(current_score)
            max_score = " ".join(['Congratulations! The maximum score is', str(min(scores))])
            client.send(max_score.encode('utf-8'))
        elif opponent == "player" and clients[1]:
            client.send('How many rounds would you like to play?'.encode('utf-8'))
            scores = []
            number_of_rounds = int(client.recv(1024).decode('utf-8'))
            for rounds in range(0, number_of_rounds):
                guessed = False
                current_score = 1
                clients[1].send(b"Give a number between 0 and 50, 0 and 50 included:")
                number_from_client = int(clients[1].recv(1024).decode('utf-8'))
                print(number_from_client)
                client.send(b"Give a number between 0 and 50, 0 and 50 included:")
                while guessed is False:
                    number = client.recv(1024).decode('utf-8')
                    print(number)
                    if int(number) == number_from_client:
                        guessed = True
                        send_all_clients(b"The guess is correct!")
                        break
                    elif int(number) < number_from_client:
                        send_all_clients(b"The number is that has to be guessed is lower...")
                        current_score = current_score + 1
                    elif int(number) > number_from_client:
                        send_all_clients(b"The number is that has to be guessed is higher...")
                        current_score = current_score + 1
                scores.append(current_score)
            max_score = " ".join(['Congratulations! The maximum score is', str(min(scores))])
            send_all_clients(max_score.encode('utf-8'))
    elif client == clients[1]:
        while True:
            continue
        '''
            try:
                message = client.recv(1024).decode('utf-8')
                send_all_clients(message)
            except:
                index = clients.index
                clients.remove(client)
                client.close()
                alias = aliases[index]
                send_all_clients(f'{alias}has left the chat room!'.encode('utf-8'))
                aliases.remove(alias)
                break
        '''


def receive():
    while True:
        print('Server is running and listening...')
        (client, address) = server.accept()
        print(f'Connection at address: {str(address)}')
        client.send('alias?'.encode('utf-8'))
        alias = client.recv(1024).decode('utf-8')
        aliases.append(alias)
        clients.append(client)
        print(f'The alias of this client is: {alias}'.encode('utf-8'));
        send_all_clients(f'{alias} has connected'.encode('utf-8'))
        client.send('you are now connected!'.encode('utf-8'))

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()


if __name__ == '__main__':
    receive()
