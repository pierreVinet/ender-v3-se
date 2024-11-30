import time
import serial


# Arduino Serial Communication
arduino_port = '/dev/tty.usbserial-110'  # Update this to the correct port (e.g., 'COM3' on Windows)
arduino_baudrate = 9600
arduino_serial = None

def initialize_arduino():
    global arduino_serial
    arduino_serial = serial.Serial(arduino_port, arduino_baudrate, timeout=1)
    time.sleep(2)  # Wait for Arduino to reset

def send_arduino_command(command):
    if arduino_serial is not None:
        arduino_serial.write((command + '\n').encode())
        time.sleep(0.1)
        response = arduino_serial.readline().decode().strip()
        print(f"Sent: {command} | Received: {response}")
        if response != "OK":
            print(f"Arduino responded with error: {response}")
    else:
        print("Arduino serial connection not initialized.")

def close_arduino():
    if arduino_serial is not None:
        arduino_serial.close()

# Define mouse positions

def main():
    initialize_arduino()

   
    # Control the servo motor
    send_arduino_command("MOVE 90")  # Move servo to 90 degrees
    time.sleep(1)
    send_arduino_command("MOVE 0")   # Move servo back to 0 degrees


    close_arduino()

main()

'''
#include <Servo.h> // Include the Servo library

Servo myServo;     // Create a Servo object

const int buttonPin = 2;  // Pin connected to the push button
int buttonState = 0;      // Variable to store the button state
int lastButtonState = 0;  // Variable to store the previous button state
int servoPosition = 0;    // Current position of the servo

void setup() {
  myServo.attach(9);      // Attach servo to pin 9
  pinMode(buttonPin, INPUT_PULLUP); // Set button pin as input with pull-up resistor
  myServo.write(servoPosition);    // Initialize servo at 0°
}

void loop() {
  buttonState = digitalRead(buttonPin); // Read the button state

  // Check if the button state has changed
  if (buttonState == LOW && lastButtonState == HIGH) { // Button is pressed
    servoPosition = (servoPosition == 0) ? 180 : 0;    // Toggle position
    myServo.write(servoPosition);                     // Move the servo
    delay(300);                                       // Debounce delay
  }

  lastButtonState = buttonState; // Save the button state
}

'''