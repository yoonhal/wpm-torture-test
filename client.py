import socket
import functions
import os

def start_client():
    host = os.getenv('IP_ADDRESS') # Use the server's IP address or 'localhost' for local testing
    port = 12345         # The port on which the server is listening

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    while True:
        data = input("Enter data to send to the server (or type 'exit' to quit): ")
        if data.lower() == 'exit':
            break

        client_socket.send(data.encode())

    client_socket.close()

if __name__ == "__main__":
    functions.configure()
    start_client()
