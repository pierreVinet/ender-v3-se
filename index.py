import serial
import time

# Replace 'COM3' with your serial port (e.g., '/dev/ttyUSB0' for Linux)
ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
time.sleep(2)  # Wait for the connection to initialize

def send_gcode(command):
    ser.write((command + '\n').encode())
    response = ser.readline().decode().strip()
    print(f"Sent: {command} | Received: {response}")
    time.sleep(0.1)  # Small delay for processing

def move_to_position(x=None, y=None, z=None, speed=3000):
    command = 'G1'
    if x is not None:
        command += f' X{x}'
    if y is not None:
        command += f' Y{y}'
    if z is not None:
        command += f' Z{z}'
    command += f' F{speed}'
    send_gcode(command)

# Wake up the printer
send_gcode('M17')  # Enable steppers
send_gcode('G90')  # Set to absolute positioning

# Example movement commands
move_to_position(x=100, y=100, z=10, speed=1000)
move_to_position(x=50, y=50, z=5, speed=1000)

ser.close()