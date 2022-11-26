import socket, time
import threading
import sys

host = '127.0.0.1'
port = 22000
print("Welcome!")
alias = input("Please type your name:")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))
client_open = True


def client_receive():
    global client_open
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == "alias?":
                client.send(alias.encode('utf-8'))
            elif message.split(' ')[0] == "Congratulations!" or message == "The other client is not connected!":
                print(message)
                client_open = False
                break
            elif message == "The player one has decided to play with a bot!":
                print(message)
                client_open = False
                break
            else:
                print(message)
        except:
            print("The server is closed")
            client.close()
            break
    client.close()


def client_send():
    while client_open is True:
        try:
            message = input()
            client.send(message.encode('utf-8'))
        except:
            print("The server is closed")
            client.close()
            break
    client.close()


if __name__ == '__main__':
    receive_thread = threading.Thread(target=client_receive)
    receive_thread.start()

    send_thread = threading.Thread(target=client_send)
    send_thread.start()
