#include <Arduino.h>

#define PLAYER1 12
#define PLAYER2 14
#define STOP 23

#define START_BUFFER 3000
#define THRESHOLD 100

char storedDataWPM[64] = "";
int player_wpm[2] = {0};
bool pause_state = true;

void parseData(char *dataStored, int *wpmValues){
  
  //create a copy of dataBuffer to avoid overwriting
  char dataCopy[64];
  strncpy(dataCopy, dataStored, sizeof(dataCopy) - 1);
  dataCopy[sizeof(dataCopy) - 1] = '\0'; 
  
  int index = 0;
  //create a token separated by comma
  char *token = strtok(dataCopy, ",");

  //looping through six tokens  
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
  Serial.begin(115200);
  pinMode(PLAYER1, OUTPUT);
  pinMode(PLAYER2, OUTPUT);
  pinMode(STOP, INPUT);
}

void loop() {

  while (pause_state) {

    if (digitalRead(STOP)) {
      pause_state = false;
      delay(START_BUFFER);
      break;
    }
  }
  
  if (Serial.available() > 0) {
    if (Serial.read() == '(') {
      storeSerialData(storedDataWPM);
    }
  }

  
  if (player_wpm[0] < THRESHOLD){
    digitalWrite(PLAYER1, HIGH);
  } else {
    digitalWrite(PLAYER1, LOW);
  }

  if (player_wpm[1] < THRESHOLD){
    digitalWrite(PLAYER2, HIGH);
  } else {
    digitalWrite(PLAYER2, LOW);
  }

  if (digitalRead(STOP)) {
    pause_state = true;
    digitalWrite(PLAYER1, LOW);
    digitalWrite(PLAYER2, LOW);
    delay(START_BUFFER);
  }

}
