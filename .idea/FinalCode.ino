#include <TimerOne.h>

float frequency = 1700; // Default frequency
float dutyCycle = 30.0; // Default duty cycle
float us; // Variable for microseconds per pulse
int sequence[] = {15000, 8500, 10000}; // Sequence for pulses and breaks

void setup() {
  Serial.begin(9600);
  pinMode(9, OUTPUT);
  updateTimer(); // Initial timer update based on default frequency and duty cycle
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n'); // Read the command until a newline
    if (command.startsWith("FREQ:")) {
      frequency = command.substring(5).toFloat(); // Extract frequency value from command
      updateTimer();
    } else if (command.startsWith("DUTY:")) {
      dutyCycle = command.substring(5).toFloat(); // Extract duty cycle value from command
      updateTimer();
    }
  }
}

void updateTimer() {
  us = (1 / frequency) * 1000000; // Calculate microseconds per pulse
  Timer1.initialize(us); // Initialize timer with updated frequency
  Timer1.pwm(9, floor((dutyCycle / 100) * 1023)); // Update PWM duty cycle
  
  // Handle sequence for pulses and breaks
  int n = sizeof(sequence) / sizeof(sequence[0]); // Calculate size of the sequence array
  for(int i = 0; i < n; i++) {
    if(i % 2 == 0) { // If even index, there will be pulses
      Timer1.setPwmDuty(9, floor((dutyCycle / 100) * 1023)); // Set duty cycle
    } else { // If odd index, there will be a break
      Timer1.setPwmDuty(9, 0); // Turn off the PWM for a break
    }
    // Apply delay for the duration specified in the sequence array
    delay(sequence[i] * us / 1000); // Convert microseconds to milliseconds for delay
    delayMicroseconds((int)sequence[i] * us % 1000); // Handle the remainder microseconds
  }

  Timer1.stop(); // Stop the timer once the sequence is completed
}
