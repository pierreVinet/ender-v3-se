import serial
import time

# Replace 'COM3' with the correct port for your Arduino
arduino_port = "COM7"
baud_rate = 9600

# Establish connection to Arduino
arduino = serial.Serial(arduino_port, baud_rate, timeout=1)

def move_servo(angle):
    if 0 <= angle <= 180:
        arduino.write(f"{angle}\n".encode())  # Send the angle as a string with newline
        print(f"Moved servo to {angle}°")
    else:
        print("Error: Angle must be between 0 and 180 degrees")

def close_arduino():
    arduino.close()

