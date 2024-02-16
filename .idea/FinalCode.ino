#include <TimerOne.h>

float frequency=1700; //sets the frequency
float dutyCycle=30.0; //sets the duty cycle
float us=(1/frequency)*1000000; //creates variable for microseconds per pulse
int sequence[]={15000,8500,10000}; //sequence for length of pulses followed by length of breaks

void setup()
{
  Serial.begin(9600);
  pinMode(9,OUTPUT);
  Timer1.initialize(us); //initializes the frequency of the wave
  int n=(sizeof(sequence)/sizeof(sequence[0])); //creates variable for the size of the input sequence
  Timer1.pwm(9,0);//initializes the timer with a duty cycle of 0 (off)
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

void loop()
{
}