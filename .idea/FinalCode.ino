#include <TimerOne.h>

float frequency = 1700; // Default frequency
float dutyCycle = 30.0; // Default duty cycle
float us; // Microseconds per pulse
int sequence[] = {15000, 8500, 10000}; // Sequence for pulses and breaks
bool sequenceRunning = false; // Flag to control sequence execution
int sequenceIndex = 0; // Tracks the current index in the sequence

void setup() {
  Serial.begin(9600);
  pinMode(9, OUTPUT);
  updateTimer(); // Initial timer update based on default frequency and duty cycle
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n'); // Read command until newline
    if (command.startsWith("FREQ:")) {
      frequency = command.substring(5).toFloat(); // Extract frequency value from command
      updateTimer();
    } else if (command.startsWith("DUTY:")) {
      dutyCycle = command.substring(5).toFloat(); // Extract duty cycle value from command
      updateTimer();
    } else if (command == "START") {
      if (!sequenceRunning) {
        sequenceRunning = true;
        runSequence(); // Start or resume
      }
    } else if (command == "STOP") {
      sequenceRunning = false; // Stop
    } else if (command == "RESET") {
      sequenceRunning = false; // Sto
      sequenceIndex = 0; 
      frequency = 1700; // Reset to default
      dutyCycle = 30.0; // Reset to default
      updateTimer();
    }
  }
}

void updateTimer() {
  us = (1 / frequency) * 1000000; // Calculate microseconds per pulse
  Timer1.initialize(us); // Initialize timer with updated frequency
  Timer1.pwm(9, floor((dutyCycle / 100) * 1023)); // Update PWM duty cycle
}

void runSequence() {
  int n = sizeof(sequence) / sizeof(sequence[0]); 
  for(; sequenceIndex < n && sequenceRunning; sequenceIndex++) {
    if(sequenceIndex % 2 == 0) { 
      Timer1.setPwmDuty(9, floor((dutyCycle / 100) * 1023)); // Set duty cycle
    } else { // If odd index, create a break
      Timer1.setPwmDuty(9, 0); // Turn off PWM for a break
    }
    // Apply delay for the duration specified in the sequence array
    delay(sequence[sequenceIndex] * us / 1000); 
    delayMicroseconds((int)sequence[sequenceIndex] * us % 1000); 
  }

  if (!sequenceRunning) { // If stopped mid-sequence, pause without resetting index
    Timer1.setPwmDuty(9, 0); // Ensure PWM is turned off if stopped
    return; // Exit the function to allow resuming later
  }

  // If sequence completed without interruption
  Timer1.stop(); 
  sequenceIndex = 0; 
  sequenceRunning = false; // Reset the running flag
}
