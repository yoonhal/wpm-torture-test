import socket
import keyboard
import time
import functions
import os


def start_server():
    host = os.getenv('IP_ADDRESS')  # Use your server's IP address or 'localhost' for local testing
    port = 12345         # Choose an available port

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print(f"Server listening on {host}:{port}")

    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address}")

    client_id = client_socket.recv(1024).decode()
    print(f"Client ID: {client_id}")

    while True:
        data = client_socket.recv(1024).decode()
        if not data:
            break
        data = functions.to_numbers(data)
        print(f"Received data from Client {client_id}: {data}")

        # Store the data in a text file with client ID
        with open(f'data_client_{client_id}.txt', 'a') as file:
            file.write(str(data) + '\n')

    client_socket.close()
    server_socket.close()

if __name__ == "__main__":
    functions.configure()
    start_server()
