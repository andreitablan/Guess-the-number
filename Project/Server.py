import socket
import threading
from random import randint
import time
import sys

host = '127.0.0.1'
port = 22000
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(2)
clients = []
aliases = []
server_open = True
adversar_is_bot = None


def send_all_clients(message):
    for client in clients:
        client.send(message)


def handle_client1(client):
    global server_open
    global adversar_is_bot
    command = True
    opponent = ""
    client.send(b"Who do you want to play with? Please type <bot> or <player>: ")
    while command is True:
        opponent = client.recv(1024).decode('utf-8')
        if opponent == "bot" or opponent == "player":
            command = False
        else:
            client.send(b"Please insert either <bot> or <player>:")

    if opponent == "bot":
        adversar_is_bot = True
        scores = []
        how_many_rounds = False
        number_of_rounds = 0
        client.send('How many rounds would you like to play (give a number between 1 and 10)?'.encode('utf-8'))
        while how_many_rounds is False:
            number_of_rounds = client.recv(1024).decode('utf-8')
            if number_of_rounds.isnumeric() and 10 >= int(number_of_rounds) >= 1:
                how_many_rounds = True
            else:
                client.send(b"Not a valid input! Please send a number between 1 and 10:")
        number_of_rounds = int(number_of_rounds)
        for rounds in range(0, number_of_rounds):
            guessed = False
            current_score = 1
            generated_number = randint(0, 50)
            print(generated_number)
            client.send(b"Give a number between 0 and 50, 0 and 50 included:")
            while guessed is False:
                is_number = False
                number = 0
                while is_number is False:
                    number = client.recv(1024).decode('utf-8')
                    if number.isnumeric() and 50 >= int(number) >= 0:
                        is_number = True
                    else:
                        client.send(b"Not a valid input! Please send a number between 0 and 50:")
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
        for client1 in clients:
            client1.close()
            print("Connection with client Closed")
        server_open = False
    elif opponent == "player" and clients[1]:
        adversar_is_bot = False
        clients[1].send(b"Please wait until the other player decides how many rounds the game will have..")
        number_of_rounds = 0
        how_many_rounds = False
        client.send('How many rounds would you like to play (give a number between 1 and 10)?'.encode('utf-8'))
        while how_many_rounds is False:
            number_of_rounds = client.recv(1024).decode('utf-8')
            if number_of_rounds.isnumeric() and 10 >= int(number_of_rounds) >= 1:
                how_many_rounds = True
            else:
                client.send(b"Not a valid input! Please send a number between 1 and 10:")
            number_of_rounds = int(number_of_rounds)
        scores = []
        for rounds in range(0, number_of_rounds):
            client.send(b"Please wait until the other player gives a number")
            guessed = False
            current_score = 1
            correct_number = False
            number_from_client = -1
            while correct_number is False:
                clients[1].send(b"Give a number between 0 and 50, 0 and 50 included:")
                number_from_client = int(clients[1].recv(1024).decode('utf-8'))
                if number_from_client > 50 or number_from_client < 0:
                    clients[1].send(b"Wrong number, the number has to be between 0 and 50!")
                else:
                    clients[1].send(b"Please wait until the other player takes a guess...")
                    correct_number = True
            client.send(b"Give a number between 0 and 50, 0 and 50 included:")
            while guessed is False:
                is_number = False
                number = 0
                while is_number is False:
                    number = client.recv(1024).decode('utf-8')
                    if number.isnumeric() and 50 >= int(number) >= 0:
                        is_number = True
                    else:
                        client.send(b"Not a valid input! Please send a number between 0 and 50:")
                print(number)
                if int(number) == number_from_client:
                    guessed = True
                    send_all_clients(b"The guess is correct!")
                    break
                elif int(number) < number_from_client:
                    send_all_clients(b"The number that has to be guessed is higher...")
                    current_score = current_score + 1
                elif int(number) > number_from_client:
                    send_all_clients(b"The number that has to be guessed is lower...")
                    current_score = current_score + 1
            scores.append(current_score)
        max_score = " ".join(['Congratulations! The maximum score is', str(min(scores))])
        send_all_clients(max_score.encode('utf-8'))
        for client1 in clients:
            client1.close()
            print("Connection with client Closed")
        server_open = False


def handle_client2(client):
    while True:
        try:
            continue
        except:
            index = clients.index
            clients.remove(client)
            client.close()
            alias = aliases[index]
            aliases.remove(alias)
            break


'''
def handle_client(client):
    global server_open
    if client == clients[0]:
        command = True
        opponent = ""
        client.send(b"Who do you want to play with? Please type <bot> or <player>: ")
        while command is True:
            opponent = client.recv(1024).decode('utf-8')
            if opponent == "bot" or opponent == "player":
                command = False
            else:
                client.send(b"Please insert either <bot> or <player>:")

        if opponent == "bot":
            scores = []
            how_many_rounds = False
            number_of_rounds = 0
            client.send('How many rounds would you like to play (give a number between 1 and 10)?'.encode('utf-8'))
            while how_many_rounds is False:
                number_of_rounds = client.recv(1024).decode('utf-8')
                if number_of_rounds.isnumeric() and 10 >= int(number_of_rounds) >= 1:
                    how_many_rounds = True
                else:
                    client.send(b"Not a valid input! Please send a number between 1 and 10:")
            number_of_rounds = int(number_of_rounds)
            for rounds in range(0, number_of_rounds):
                guessed = False
                current_score = 1
                generated_number = randint(0, 50)
                print(generated_number)
                client.send(b"Give a number between 0 and 50, 0 and 50 included:")
                while guessed is False:
                    is_number = False
                    number = 0
                    while is_number is False:
                        number = client.recv(1024).decode('utf-8')
                        if number.isnumeric() and 50 >= int(number) >= 0:
                            is_number = True
                        else:
                            client.send(b"Not a valid input! Please send a number between 0 and 50:")
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
            for client1 in clients:
                client1.close()
                print("Connection with client Closed")
            server_open = False

        elif opponent == "player" and clients[1]:
            clients[1].send(b"Please wait until the other player decides how many rounds the game will have..")
            number_of_rounds = 0
            how_many_rounds = False
            client.send('How many rounds would you like to play (give a number between 1 and 10)?'.encode('utf-8'))
            while how_many_rounds is False:
                number_of_rounds = client.recv(1024).decode('utf-8')
                if number_of_rounds.isnumeric() and 10 >= int(number_of_rounds) >= 1:
                    how_many_rounds = True
                else:
                    client.send(b"Not a valid input! Please send a number between 1 and 10:")
                number_of_rounds = int(number_of_rounds)
            scores = []
            for rounds in range(0, number_of_rounds):
                client.send(b"Please wait until the other player gives a number")
                guessed = False
                current_score = 1
                correct_number = False
                number_from_client = -1
                while correct_number is False:
                    clients[1].send(b"Give a number between 0 and 50, 0 and 50 included:")
                    number_from_client = int(clients[1].recv(1024).decode('utf-8'))
                    if number_from_client > 50 or number_from_client < 0:
                        clients[1].send(b"Wrong number, the number has to be between 0 and 50!")
                    else:
                        clients[1].send(b"Please wait until the other player takes a guess...")
                        correct_number = True
                client.send(b"Give a number between 0 and 50, 0 and 50 included:")
                while guessed is False:
                    is_number = False
                    number = 0
                    while is_number is False:
                        number = client.recv(1024).decode('utf-8')
                        if number.isnumeric() and 50 >= int(number) >= 0:
                            is_number = True
                        else:
                            client.send(b"Not a valid input! Please send a number between 0 and 50:")
                    print(number)
                    if int(number) == number_from_client:
                        guessed = True
                        send_all_clients(b"The guess is correct!")
                        break
                    elif int(number) < number_from_client:
                        send_all_clients(b"The number that has to be guessed is higher...")
                        current_score = current_score + 1
                    elif int(number) > number_from_client:
                        send_all_clients(b"The number that has to be guessed is lower...")
                        current_score = current_score + 1
                scores.append(current_score)
            max_score = " ".join(['Congratulations! The maximum score is', str(min(scores))])
            send_all_clients(max_score.encode('utf-8'))
            for client1 in clients:
                client1.close()
                print("Connection with client Closed")
            server_open = False

    elif client == clients[1]:
        while True:
            try:
                continue
            except:
                index = clients.index
                clients.remove(client)
                client.close()
                alias = aliases[index]
                aliases.remove(alias)
                break
'''


def receive():
    while server_open is True:
        print('Server is running and listening...')
        (client, address) = server.accept()
        print(f'Connection at address: {str(address)}')
        client.send('alias?'.encode('utf-8'))
        alias = client.recv(1024).decode('utf-8')
        aliases.append(alias)
        clients.append(client)
        print(f'The alias of this client is: {alias}'.encode('utf-8'));
        client.send('Welcome in the game! Please wait...'.encode('utf-8'))
        if client == clients[0]:
            thread = threading.Thread(target=handle_client1, args=(client,))
            thread.start()
        if adversar_is_bot is False:
            thread = threading.Thread(target=handle_client2, args=(client,))
            thread.start()
            break

    print("server closed")
    server.close()


if __name__ == '__main__':
    receive()
