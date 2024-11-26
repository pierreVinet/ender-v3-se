import serial
import time

ser = None
port = 'COM9'

def initialize_port():
    global ser

    # Replace 'COM7' with your serial port (e.g., '/dev/ttyUSB0' for Linux)
    ser = serial.Serial(port, 115200, timeout=1)
    time.sleep(2)  # Wait for the connection to initialize

def send_gcode(command):
    ser.write((command + '\n').encode())
    response = ser.readline().decode().strip()
    print(f"Sent: {command} | Received: {response}")
    time.sleep(0.1)  # Small delay for processing

def move_to_position(x=None, y=None, z=None, speed=3000):
    send_gcode('G90')  # Ensure absolute positioning
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
    send_gcode('M302 S0')  # Allow cold extrusion
    send_gcode('G91')  # Ensure relative positioning
    command = f'G1 E{e} F{speed}'
    send_gcode(command)
    

def close_connection():
    ser.close()

