import socket
import threading
import inspect
from random import randint

host = '127.0.0.1'
port = 22001
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(2)
clients = []
aliases = []
server_open = True
opponent_is_bot = 0


def set_global_opponent(value):
    """

    The global variable is useful is the player one wants to play with a bot and the player two is connected.
    Args:
        value: the value that is to be set for the global variable

    Returns:nothing

    """
    global opponent_is_bot
    opponent_is_bot = value


def send_all_clients(message):
    """

    Sends a message to all the clients.
    Args:
        message:The message that has to be sent to all the clients

    Returns:nothing

    """
    for client in clients:
        client.send(message)


def get_opponent_from_client1():
    """

    Gets the opponent from player 1.
    Returns: The opponent decided by the player 1.(bot or player)

    """
    command = True
    opponent = ""
    clients[0].send(b"Who do you want to play with? Please type <bot> or <player>: ")
    while command is True:
        opponent = clients[0].recv(1024).decode('utf-8')
        if opponent == "bot" or opponent == "player":
            command = False
        else:
            clients[0].send(b"Please insert either <bot> or <player>:")
    return opponent


def get_number_of_rounds_from_client1():
    """

    Gets number of rounds from player 1.
    Returns:The number of rounds the player one has decided to play.

    """
    how_many_rounds = False
    number_of_rounds = 0
    clients[0].send('How many rounds would you like to play (give a number between 1 and 10)?'.encode('utf-8'))
    while how_many_rounds is False:
        number_of_rounds = clients[0].recv(1024).decode('utf-8')
        if number_of_rounds.isnumeric() and 10 >= int(number_of_rounds) >= 1:
            how_many_rounds = True
        else:
            clients[0].send(b"Not a valid input! Please send a number between 1 and 10:")
    number_of_rounds = int(number_of_rounds)
    return number_of_rounds


def finish_game_with_bot(score):
    """

    Sends the score to the player 1.
    Args:
        score: The final score of the game.

    Returns:nothing

    """
    global server_open
    max_score = " ".join(['Congratulations! The maximum score is', score])
    clients[0].send(max_score.encode('utf-8'))
    for client1 in clients:
        client1.close()
        print("Connection with client Closed")
    server_open = False


def finish_game_with_player(score):
    """

    Sends the final score to all the players.
    Args:
        score: The final score of the game

    Returns:nothing

    """
    global server_open
    max_score = " ".join(['Congratulations! The maximum score is', score])
    send_all_clients(max_score.encode('utf-8'))
    for client1 in clients:
        client1.close()
        print("Connection with client Closed")
    server_open = False


def guess_number(number_to_be_guessed):
    """

    Ask the player 1 to send a number until his guess is correct.
    Args:
        number_to_be_guessed: The number that has to be guessed in each round.

    Returns: The number of times he guessed.

    """
    guessed = False
    current_score = 1
    print("The number to be guessed is: " + str(number_to_be_guessed))
    clients[0].send(b"Give a number between 0 and 50, 0 and 50 included:")
    while guessed is False:
        is_number = False
        number = 0
        while is_number is False:
            number = clients[0].recv(1024).decode('utf-8')
            if number.isnumeric() and 50 >= int(number) >= 0:
                is_number = True
            else:
                clients[0].send(b"Not a valid input! Please send a number between 0 and 50:")
        print("The client's guess is: " + str(number))
        if int(number) == number_to_be_guessed:
            guessed = True
            clients[0].send(b"The number is correct!")
            break
        elif int(number) < number_to_be_guessed:
            clients[0].send(b"The number you sent is lower than the number you have to guess...Guess again!")
            current_score = current_score + 1
        elif int(number) > number_to_be_guessed:
            clients[0].send(b"The number you sent is higher then the number you have to guess...Guess again!")
            current_score = current_score + 1
    return current_score


def get_number_to_be_guessed_from_client():
    """

    Asks the player 2 to give a number.
    Returns:The number that the player two gave.

    """
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
    return number_from_client


def play_with_bot():
    """

    This method is used when player one decided to play with a bot.
    Returns: nothing

    """
    scores = []
    number_of_rounds = get_number_of_rounds_from_client1()
    for rounds in range(0, number_of_rounds):
        number_to_be_guessed = randint(0, 50)
        current_score = guess_number(number_to_be_guessed)
        scores.append(current_score)
    finish_game_with_bot(str(min(scores)))


def play_with_player():
    """

    This method is used when player one decided to play with a player.
    Returns: nothing

    """
    scores = []
    clients[1].send(b"Please wait until the other player decides how many rounds the game will have..")
    number_of_rounds = get_number_of_rounds_from_client1()
    for rounds in range(0, number_of_rounds):
        clients[0].send(b"Please wait until the other player gives a number")
        number_from_client = get_number_to_be_guessed_from_client()
        current_score = guess_number(number_from_client)
        scores.append(current_score)
    finish_game_with_player(str(min(scores)))


def handle_client1():
    """

    Handles the request for the player one.
    Returns:nothing.

    """
    opponent = get_opponent_from_client1()

    if opponent == "bot":
        set_global_opponent(1)
        play_with_bot()

    elif opponent == "player":
        try:
            clients[1].send(b"The player 1 has decided to play with you!")
            play_with_player()
        except:
            clients[0].send(b"The other client is not connected!")
            print("The client 1 wanted to play with another player, but he is not connected!")
            global server_open
            server_open = False
            return


def handle_client2():
    """

    Handles the requests for player two.
    Returns:nothing

    """
    while opponent_is_bot == 0:
        try:
            continue
        except:
            index = clients.index
            clients.remove(clients[1])
            clients[1].close()
            alias = aliases[index]
            aliases.remove(alias)
            break
    clients[1].send(b"The player one has decided to play with a bot!")
    print("The player two wants to play, but the player one decided to play with a bot!")


def receive():
    """

    Handles the server and waits for the clients.
    Returns:nothing

    """
    global server_open
    while server_open is True:
        print('Server is running and listening...')
        if server_open:
            (client, address) = server.accept()
        print(f'Connection at address: {str(address)}')
        client.send('alias?'.encode('utf-8'))
        alias = client.recv(1024).decode('utf-8')
        aliases.append(alias)
        clients.append(client)
        print(f'The alias of this client is: {alias}'.encode('utf-8'));
        client.send('Welcome in the game! Please wait...'.encode('utf-8'))
        if client == clients[0]:
            thread = threading.Thread(target=handle_client1, args=())
            thread.start()
        else:
            thread = threading.Thread(target=handle_client2, args=())
            thread.start()
            server_open = False
            break
    print("Server not accepting more clients!")
    server.close()


if __name__ == '__main__':
    receive()
