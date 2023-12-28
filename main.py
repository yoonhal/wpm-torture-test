from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import keyboard
import socket
import uuid
import os
import functions


# Main program - open monkeytype and start receiving/sending data
def wpm_run():
    print("--- PROGRAM START ---")

    # Options Setup
    options = Options()
    options.headless = True
    options.add_argument("start-maximized")

    # Webdriver Start
    driver = webdriver.Chrome(options = options)
    driver.get("https://monkeytype.com/")
    print("Connected to monkeytype.")

    # WiFi Setup
    host = os.getenv('IP_ADDRESS') # Server's IP Address
    port = 12345       

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    # Generate a unique client ID
    client_id = str(uuid.uuid4())
    client_socket.send(client_id.encode())

    # Get WPM Data
    try:
        while True:
            # WPM on monkeytype updates every 1 sec
            time.sleep(1)

            # Current HTML of the page
            page_source = driver.page_source

            # Parsing the HTML 
            soup = BeautifulSoup(page_source, 'html.parser')
    
            player_wpm = functions.to_numbers(soup.find('div', class_='wpm hidden')) 
    
            if (player_wpm == 0):
                print("Please Start Typing!")
            else:
                print(f"Current WPM is: {player_wpm}")
        

            # Send player data to server
            try:
                client_socket.send(str(player_wpm).encode())
            except ValueError:
                print("Invalid value")

            # HOLD "esc" to exit
            if keyboard.is_pressed('esc'):
                driver.quit()
                client_socket.close()
                #ser.close()
                break

    except Exception as e:
        print(f"An error occurred: {e}")
        driver.quit()
         #ser.close()
        
    print("--- PROGRAM END ---")


if __name__ == "__main__":
    functions.configure()
    wpm_run()