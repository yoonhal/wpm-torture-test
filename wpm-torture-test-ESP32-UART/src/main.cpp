#include <Arduino.h>

// pin setup
#define PLAYER1 12
#define PLAYER2 14
#define STOP 23
#define LED 2

// game constants
#define START_BUFFER 3000 // short buffer before start of game
#define THRESHOLD 120 // game ends when level reaches 120 WPM
#define LEVEL_INCREASE 10 // increases by 10 WPM every level
#define LEVEL_TIMER 15000 // 15 seconds
#define LED_TIMER 1000 // 1 second

char storedDataWPM[64] = "";
int player_wpm[2] = {0};

bool pause_state = true;
int level_wpm = 50; // starts at 50 WPM
unsigned long prev_time; // track elapsed time
unsigned long current_time; // track elapsed time

// parses data received by UART
void parseData(char *dataStored, int *wpmValues){
  
  // create a copy of dataBuffer to avoid overwriting
  char dataCopy[64];
  strncpy(dataCopy, dataStored, sizeof(dataCopy) - 1);
  dataCopy[sizeof(dataCopy) - 1] = '\0'; 
  
  int index = 0;
  // create a token separated by comma
  char *token = strtok(dataCopy, ",");

  // looping through six tokens  
  while (token != NULL && index < 2){
    wpmValues[index] = atoi(token);
    token = strtok(NULL, ",");
    index++;
  }

  if (index == 2){
    Serial.println("Data extraction successful!");
  } else {
    Serial.println("Error.");
  }
}

// stores data from UART
void storeSerialData(char *charArray) {
  int count = 0;

  while (Serial.available() > 0) {
    char tempChar = Serial.read();
    if (tempChar == ')') {
      charArray[count] = '\0';
      break;
    }
    charArray[count] = tempChar;
    count++;
  }

  Serial.println(charArray);
  parseData(storedDataWPM, player_wpm);
  Serial.println(player_wpm[0]);
  Serial.println(player_wpm[1]);
}


void setup() {
  // start serial
  Serial.begin(115200);

  // pin mode config
  pinMode(PLAYER1, OUTPUT);
  pinMode(PLAYER2, OUTPUT);
  pinMode(STOP, INPUT);
  pinMode(LED, OUTPUT);

  // indicate set up completion
  digitalWrite(LED, LOW);
  delay(100);
  digitalWrite(LED, HIGH);
  delay(100);
  digitalWrite(LED, LOW);
}


void loop() {

  // pre-game state, click button to start
  while (pause_state) {

    if (digitalRead(STOP)) {
      pause_state = false;
      delay(START_BUFFER);
      // set timer
      prev_time = millis();
      break;
    }
  }
  
  // Take time of current loop
  current_time = millis();

  // Determine if we increase level (time passed LEVEL_TIMER)
  if (current_time - prev_time > LEVEL_TIMER && level_wpm <= THRESHOLD) {
    // Increase level wpm
    level_wpm += LEVEL_INCREASE;

    // indicate level change through built in LED
    digitalWrite(LED, HIGH);

    // reset timer for level
    prev_time = current_time;
  }
  else {
    // if last level has been reaeched, restart game
    digitalWrite(PLAYER1, LOW);
    digitalWrite(PLAYER2, LOW);
    level_wpm = 50;
    pause_state = true;
  }

  // turn level indicator LED off
  if (current_time - prev_time > LED_TIMER) {
    digitalWrite(LED, LOW);
  }

  // pull and parse data from server through UART
  if (Serial.available() > 0) {
    if (Serial.read() == '(') {
      storeSerialData(storedDataWPM);
    }
  }

  // check if player 1 is below level minimum wpm
  if (player_wpm[0] < level_wpm){
    // shock if less than
    digitalWrite(PLAYER1, HIGH);
  } else {
    // no shock if greater or equal
    digitalWrite(PLAYER1, LOW);
  }

  // check if player 2 is below level minimum wpm
  if (player_wpm[1] < level_wpm){
    // shock if less than
    digitalWrite(PLAYER2, HIGH);
  } else {
    // no shock if greater or equal
    digitalWrite(PLAYER2, LOW);
  }

  // pause game if stop button has been pressed
  if (digitalRead(STOP)) {
    pause_state = true;
    digitalWrite(PLAYER1, LOW);
    digitalWrite(PLAYER2, LOW);
    delay(START_BUFFER);
  }


}
