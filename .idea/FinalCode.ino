#include <TimerOne.h>
#include <string.h>

const byte numChars = 32;
char receivedChars[numChars];
char tempChars[numChars];        // temporary array for use when parsing

      // variables to hold the parsed data
float frequency=1;
float dutyCycle = 0;
int sequence[] = {};
int sequenceSize=0;

boolean newData = false;

float us=(1/frequency)*1000000; //creates variable for microseconds per pulse

void setup()
{
  Serial.begin(9600);
  pinMode(9,OUTPUT);
  Timer1.initialize(us); //initializes the frequency of the wave
  Timer1.pwm(9,0);//initializes the timer with a duty cycle of 0 (off)
}

void loop()
{
  recvWithStartEndMarkers();
    if (newData == true) {
        strcpy(tempChars, receivedChars);
            // this temporary copy is necessary to protect the original data
            //   because strtok() used in parseData() replaces the commas with \0
        parseData();
        newData = false;
    }
  int n=(sizeof(sequence)/sizeof(sequence[0])); //creates variable for the size of the input sequence
  if(sizeof(sequence)==0){
  while(sizeof(sequence)==0){
    Timer1.setPwmDuty(9,floor((dutyCycle/100)*1023));
  }}
  else{
    Serial.println("next");
  for(int i=0;i<n;i=i+1){
    Serial.println(i);
    if(i%2==0){//sets so if sequence is on an even index there will pulses, and if on an odd index there will be a break
      Timer1.setPwmDuty(9,floor((dutyCycle/100)*1023));//Sets the duty cycle of the timer to be the duty cycle the user input
      delay(((int)sequence[i]*us)/1000); //delays for the number of pulses in sequence multiplied by the microseconds per pulse, then divided into ms and us
      delayMicroseconds(((int)floor(sequence[i]*us))%1000); //us portion of the delay, delayMicrosecond is only accurate to 16383 us, so easier to have an accurate ms delay and add on the us delay
    }
    else{
      Timer1.setPwmDuty(9,0);//sets a break
      delay(((int)sequence[i]*us)/1000);//same timing as before
      delayMicroseconds(((int)floor(sequence[i]*us))%1000);
    }
  }
  Timer1.setPwmDuty(9,0);
  delay(10);
  Timer1.stop();//stops the timer once the sequence has run once, may add a parameter for repeating the sequence a certain number of times later
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

    strtokIndx = strtok(tempChars,"\r");      // get the first part
    sequenceSize = atoi(strtokIndx); // copy the first part of the string to be the integer size of sequence

    strtokIndx = strtok(NULL,"\r"); // this continues where the previous call left off
    frequency = atof(strtokIndx); //copy the second part of the string to be the frequency float

    strtokIndx = strtok(NULL, "\r"); 
    dutyCycle = atof(strtokIndx);     // copy the third part of the string to be the dutyCycle float

    int templen=sequenceSize; //temp variable for indexing
    while(templen>0){//loop that will cobvert all subsequent values in the string into members of the sequence
      strtokIndx = strtok(NULL, "\r");     
      sequence[sequenceSize-templen]=atoi(strtokIndx); //assigns the next part of sequence to be whatever value is next
      templen=templen-1;//reduces temp variable to continue down the string
    }
}
