#include <TimerOne.h>
#include <string.h>

const byte numChars = 32;
char receivedChars[numChars];
char tempChars[numChars];        // temporary array for use when parsing

      // variables to hold the parsed data
float frequency=1700;
float dutyCycle = 10;
int sequence[] = {12,6};
int sequenceSize=2;

boolean newData = true;


void setup()
{
  Serial.begin(9600);
  pinMode(3,OUTPUT);
}

void loop()
{
  analogWriteFrequency(3, frequency); //initializes the frequency of the wave
  analogWrite(3, 0);;//initializes the timer with a duty cycle of 0 (off)
  int n=(sizeof(sequence)/sizeof(sequence[0])); //creates variable for the size of the input sequence
  if(sizeof(sequence)==0){
  while(sequenceSize==0){
    analogWrite(3,floor((dutyCycle/100)*256));
  }}
  else{
    Serial.println("next");
  for(int i=0;i<n;i=i+1){
    Serial.println(i);
    if(i%2==0){//sets so if sequence is on an even index there will pulses, and if on an odd index there will be a break
      analogWrite(3,floor((dutyCycle/100)*256));//Sets the duty cycle of the timer to be the duty cycle the user input
      delay((int)sequence[i]); //delays for the number of pulses in sequence multiplied by the microseconds per pulse, then divided into ms and us
      delayMicroseconds((int)((float)sequence[i]-floor(sequence[i]))*1000); //us portion of the delay, delayMicrosecond is only accurate to 16383 us, so easier to have an accurate ms delay and add on the us delay
    }
    else{
      analogWrite(3,0);//sets a break
      delay((int)sequence[i]);//same timing as before
      delayMicroseconds((int)((float)sequence[i]-floor(sequence[i]))*1000);
    }
  }
  analogWrite(3,0);
  }
}
