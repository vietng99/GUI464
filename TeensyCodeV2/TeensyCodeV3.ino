#include <TimerOne.h>
#include <string.h>

const byte numChars = 64;  // Increased buffer size for longer messages
char receivedChars[numChars];
char tempChars[numChars];        

float frequency = 0;
float dutyCycle = 0;
int sequence[32];  // Ensure this is sized to handle your expected sequence length
int sequenceSize = 0;

int threshold=341;
int val;

boolean newData = false;

void setup() {
    Serial.begin(9600);
    pinMode(3, OUTPUT);
}

void loop() {
    val=analogRead(A8);
    while(val<threshold){
      analogWrite(3, 0);
      val=analogRead(A8);
      delay(1);
    }
    threshold=-1;
    recvWithStartEndMarkers();
    if (newData == true) {
        strcpy(tempChars, receivedChars);
        parseData();
        Serial.println("Data Received and Parsed");  // Acknowledgment message
        newData = false;
    }
  analogWriteFrequency(3, frequency); //initializes the frequency of the wave
  analogWrite(3, 0);//initializes the timer with a duty cycle of 0 (off)
  int n=(sizeof(sequence)/sizeof(sequence[0])); //creates variable for the size of the input sequence
  if(sizeof(sequence)==0){
  while(sequenceSize==0){
    analogWrite(3,floor((dutyCycle/100)*256));
  }}
  else{
    Serial.println("next");
  for(int i=0;i<n;i=i+1){
    if(i%2==0){//sets so if sequence is on an even index there will pulses, and if on an odd index there will be a break
      analogWrite(3,floor((dutyCycle/100)*256));//Sets the duty cycle of the timer to be the duty cycle the user input
      delay((int)(sequence[i]/1000)); //delays for the number of pulses in sequence multiplied by the microseconds per pulse, then divided into ms and us
      delayMicroseconds((int)((sequence[i])%1000)); //us portion of the delay, delayMicrosecond is only accurate to 16383 us, so easier to have an accurate ms delay and add on the us delay
    }
    else{
      analogWrite(3,0);//sets a break
      delay((int)(sequence[i]/1000)); //same timing as before
      delayMicroseconds((int)((sequence[i])%1000));
    }
  }
  analogWrite(3,0);
  }
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
        }
    }
}

void parseData() {      // split the data into its parts

    char * strtokIndx; // this is used by strtok() as an index

    strtokIndx = strtok(tempChars,",");      // get the first part
    sequenceSize = atoi(strtokIndx); // copy the first part of the string to be the integer size of sequence
    Serial.print("check1");
    strtokIndx = strtok(NULL,","); // this continues where the previous call left off
    frequency = atof(strtokIndx); //copy the second part of the string to be the frequency float
    Serial.print("check2");
    strtokIndx = strtok(NULL, ","); 
    dutyCycle = atof(strtokIndx);     // copy the third part of the string to be the dutyCycle float
    Serial.print("check3");
    int templen=sequenceSize; //temp variable for indexing
    while(templen>0){//loop that will cobvert all subsequent values in the string into members of the sequence
      strtokIndx = strtok(NULL, ",");     
      sequence[sequenceSize-templen]=atoi(strtokIndx); //assigns the next part of sequence to be whatever value is next
      templen=templen-1;//reduces temp variable to continue down the string
    }
}
