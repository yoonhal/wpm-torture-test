import socket
import keyboard
import time
import functions
import os
import serial


def start_server():
    # init player data
    WPM_data = "(0,0)"

    # User selects mode (Single-Player or Versus)
    print("Single-Player Mode (type '1') or Versus Mode (type '2')? ")

    while True:
        mode = functions.to_numbers(input())

        if mode == 1:
            print(f"You selected Single-Player mode.")
            break
        elif mode == 2:
            print("You selected Versus Mode.")
            break
        else:
            print("Please enter a valid  mode!")

    # Start Server and wait for player connection(s)
    host = os.getenv('IP_ADDRESS')  # Use your server's IP address or 'localhost' for local testing
    port = 12345         # Choose an available port

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print(f"Server listening on {host}:{port}")

    # Find Player(s)
    player1_socket, player1_address = server_socket.accept()
    print(f"Connection from {player1_address} as Player-1")

    player1_id = player1_socket.recv(1024).decode()
    print(f"Player-1 ID: {player1_id}")

    print("Waiting for Player-2...")
    
    if mode == 2:
        player2_socket, player2_address = server_socket.accept()
        print(f"Connection from {player2_address} as Player-2")

        player2_id = player2_socket.recv(1024).decode()
        print(f"Player-2 ID: {player2_id}")

    # Init serial communcations with ESP32
    serial_port = 'COM7'
    baud_rate = 115200

    # Open serial connection
    ser = serial.Serial(port=serial_port, baudrate=baud_rate)
    time.sleep(2)

    while True:
        player1_data = player1_socket.recv(1024).decode()
        if not player1_data:
            break
        player1_data = functions.to_numbers(player1_data)
        print(f"Player-1: {player1_data} WPM")
        WPM_data = f"({player1_data},0)"

        # Repeat for Player-2 if Versus mode
        if mode == 2:
            player2_data = player2_socket.recv(1024).decode()
            if not player2_data:
                break
            player2_data = functions.to_numbers(player2_data)
            print(f"Player-2: {player2_data} WPM")
            WPM_data = f"({player1_data},{player2_data})"


        

        # Send Data to ESP32 via UART
        ser.write(WPM_data.encode('utf-8'))

        # Read response
        #response = ser.readline().decode('utf-8')

    player1_socket.close()
    if mode == 2:
        player2_socket.close()
    server_socket.close()
    ser.close()

    print("--- SERVER DISCONNECTED ---")

if __name__ == "__main__":
    functions.configure()
    start_server()
