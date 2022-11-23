import socket, time
import threading
import sys

host = '127.0.0.1'
port = 22000
print("Welcome!")
alias = input("Please type your name:")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))


def client_receive():
    while True:
        message = client.recv(1024).decode('utf-8')
        if message == "alias?":
            client.send(alias.encode('utf-8'))

        elif message.split(' ')[0] == "Congratulations!":
            print(message)
            print('Thank you for playing the game!')
            client.close()
            exit(0)
            break
        else:
            print(message)


def client_send():
    while True:
        message = input()
        client.send(message.encode('utf-8'))


if __name__ == '__main__':
    receive_thread = threading.Thread(target=client_receive)
    receive_thread.start()

    send_thread = threading.Thread(target=client_send)
    send_thread.start()
