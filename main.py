from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import keyboard
import socket
import uuid
import serial
from dotenv import load_dotenv
import os
import functions

# Configurations
def configure():
    load_dotenv()


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
    
            wpm = functions.to_numbers(soup.find('div', class_='wpm hidden')) 
    
            if (wpm == 0):
                print("Please Start Typing!")
            else:
                print(f"Current WPM is: {wpm}")
        

            # TODO communicate to Server
            try:
                client_socket.send(str(wpm).encode())
            except ValueError:
                print("Invalid value")

            # Send Data to ESP32 via UART
            # try:
            #     # Send data
            #     ser.write(wpm.encode('utf-8'))

            #     # Read response
            #     #response = ser.readline().decode('utf-8')

            # finally:
            #     print("data sent")

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
    configure()
    wpm_run()