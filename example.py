import serial
import time


port = 'COM9'
# Replace 'COM3' with your serial port (e.g., '/dev/ttyUSB0' for Linux)
ser = serial.Serial(port, 115200, timeout=1)
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

def home_axes(axes=''):
    command = f'G28 {axes}'.strip()
    send_gcode(command)


def move_extruder(e, speed=300):
    command = f'G1 E{e} F{speed}'
    send_gcode(command)

# Wake up the printer
send_gcode('M17')  # Enable steppers
send_gcode('G90')  # Set to absolute positioning

# Home all axes
home_axes()

# Example movement commands
# move_to_position(x=120, y=100, z=50, speed=600)

# Rotate the extruder motor
send_gcode('M302 S0')  # Allow cold extrusion
send_gcode('G91')      # Set to relative positioning for extruder movement
move_extruder(10, speed=300)  # Extrude 10 units of filament
send_gcode('G90')      # Set back to absolute positioning

ser.close()