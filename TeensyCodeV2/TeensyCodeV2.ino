#include <TimerOne.h>
#include <string.h>

const byte numChars = 32;
char receivedChars[numChars];   // an array to store the received data
char tempChars[numChars];       // temporary array for use when parsing

// Variables to hold the parsed data
float frequency = 200;
float dutyCycle = 50;
int sequence[10]; // Adjust the size according to your needs
int sequenceSize = 0;

boolean newData = false;

unsigned long previousMillis = 0; // will store last time LED was updated
unsigned long sequenceStartTime = 0; // Start time of the sequence
unsigned long sequenceDuration = 0; // Duration for the sequence to run, in milliseconds
const long interval = 1000;       // interval at which to blink (milliseconds)
int sequenceIndex = 0;            // Index to track the current position in the sequence

void setup() {
    Serial.begin(9600);
    pinMode(3, OUTPUT);
}

void loop() {
    recvWithStartEndMarkers();
    if (newData == true) {
        if (strcmp(receivedChars, "<STOP>") == 0) {
            stopSequence();
        } else if (strcmp(receivedChars, "<RESET>") == 0) {
            resetSequence();
        } else {
            strcpy(tempChars, receivedChars);
            parseData();
            sequenceIndex = 0; // Reset sequence index for new execution
        }
        newData = false;
    }
    executeSequence();
}

void recvWithStartEndMarkers() {
    static boolean recvInProgress = false;
    static byte ndx = 0;
    char startMarker = '<';
    char endMarker = '>';
    char rc;
  
    while (Serial.available() > 0 && newData == false) {
        rc = Serial.read();
        if (recvInProgress == true) {
            if (rc != endMarker) {
                receivedChars[ndx] = rc;
                ndx++;
                if (ndx >= numChars) {
                    ndx = numChars - 1;
                }
            }
            else {
                receivedChars[ndx] = '\0'; // terminate the string
                recvInProgress = false;
                ndx = 0;
                newData = true;
            }
        }
        else if (rc == startMarker) {
            recvInProgress = true;
            ndx = 0;
        }
    }
}

void parseData() { // Split the data into its parts
    char *strtokIndx; // this is used by strtok() as an index
  
    strtokIndx = strtok(tempChars, ",");
    sequenceSize = atoi(strtokIndx);
  
    strtokIndx = strtok(NULL, ",");
    frequency = atof(strtokIndx);
  
    strtokIndx = strtok(NULL, ",");
    dutyCycle = atof(strtokIndx);
  
    int i = 0;
    while((strtokIndx = strtok(NULL, ",")) != NULL && i < sequenceSize) {
        sequence[i++] = atoi(strtokIndx);
    }
    // Adjust sequence size if less data was provided
    sequenceSize = i;
    strtokIndx = strtok(NULL, ",");
    sequenceDuration = (unsigned long)atol(strtokIndx);
    sequenceStartTime = millis(); // Start time of the sequence
}

void stopSequence() {
    // Implement stop logic here, e.g., turn off the output immediately
    analogWrite(3, 0); // Example of turning off the output
    Serial.println("Sequence Stopped");
}

void resetSequence() {
    // Reset variables to default values
    frequency = 200;
    dutyCycle = 50;
    sequenceSize = 0;
    Serial.println("Sequence Reset");
}

void executeSequence() {
    // Check if there's a sequence to execute and if the sequence index is within bounds
    if (sequenceSize > 0 && sequenceIndex < sequenceSize) {
        // Check if the specified duration has elapsed
        if (millis() - sequenceStartTime > sequenceDuration) {
            stopSequence(); // Stop the sequence if the duration has elapsed
            sequenceSize = 0; // Prevent further execution until new data is received
            Serial.println("Sequence duration elapsed, stopping");
            return; // Exit the function to avoid further execution
        }

        unsigned long currentMillis = millis();
        if (currentMillis - previousMillis >= interval) {
            previousMillis = currentMillis;
            // Execute the current step in the sequence
            if (sequenceIndex % 2 == 0) {
                // Active step - turn on the output with the specified duty cycle
                analogWrite(3, (int)(dutyCycle / 100 * 255));
            } else {
                // Pause step - turn off the output
                analogWrite(3, 0);
            }
            Serial.print("Executing step: ");
            Serial.println(sequenceIndex);
            sequenceIndex++;
            if (sequenceIndex >= sequenceSize) {
                sequenceIndex = 0; // Optionally, reset to start or completely stop execution
            }
        }
    }
}