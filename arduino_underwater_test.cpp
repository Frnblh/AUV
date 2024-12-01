#include <Servo.h>

Servo esc1; // Stern Port Thruster
Servo esc2; // Stern Starboard Thruster
Servo esc3; // Bow Port Thruster
Servo esc4; // Bow Starboard Thruster
Servo esc56; // Heave Port and Starboard Thrusters

unsigned long startTime; // Variable to store the start time
const unsigned long runDuration = 120000; // 2 minutes in milliseconds

void setup() {
  // Attach each ESC to its respective pin

  esc1.attach(3); // Attached to Pin 3    Stern
  esc2.attach(5); // Attached to Pin 5    Stern


  esc3.attach(6); // Attached to Pin 6    Bow
  esc4.attach(9); // Attached to Pin 9    Bow
  
  esc56.attach(11); // Attached to Pin 11 Heave

  delay(2000);   // Delay to wait for all ESCs to initialize

  // Send minimum pulse to calibrate all ESCs
  esc1.writeMicroseconds(1000);
  esc2.writeMicroseconds(1000);
  esc3.writeMicroseconds(1000);
  esc4.writeMicroseconds(1000);

  esc56.writeMicroseconds(1500);

  delay(2000);   // Delay to allow ESCs to calibrate
  startTime = millis(); // Record the start time
}

void loop() {
  unsigned long currentTime = millis();

  // Check if 2 minutes have passed
  if (currentTime - startTime < runDuration) {
    // Set ESCs to desired values
    esc56.writeMicroseconds(2000); // Start heave
    delay(2000); // Wait 2 sec

    // Start stern thrusters
    esc1.writeMicroseconds(2000);
    esc2.writeMicroseconds(2000);
    delay(2000); // Wait 2 sec

    // Start bow thrusters
    esc3.writeMicroseconds(1000);
    esc4.writeMicroseconds(2000);
    delay(2000); // Wait 2 sec
  } else {
    // Stop all thrusters after 2 minutes
    esc1.writeMicroseconds(1000);
    esc2.writeMicroseconds(1000);
    esc3.writeMicroseconds(1000);
    esc4.writeMicroseconds(1000);
    esc56.writeMicroseconds(1500);

    // End loop execution
    while (true) {
      // Stay here until power is cycled
    }
  }
}