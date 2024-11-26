import serial
import time
import json

ser = None  # Global variable to hold the serial connection
processing = False
port = 'COM7'

def initialize_port():
    global ser
    # Replace 'COM7' with your serial port (e.g., '/dev/ttyUSB0' for Linux)
    ser = serial.Serial(port, 115200, timeout=1)
    time.sleep(2)  # Wait for the connection to initialize

def send_gcode(command):
    global processing
    ser.write((command + '\n').encode())
    while True:
        response = ser.readline().decode().strip()
        if response:
            if 'processing' in response:
                if processing == False:
                    print(f"Sent: {command} | Received: processing ...")
                    processing = True
            if response == 'ok':
                print(f"Sent: {command} | Received: {response}")
                processing = False
                break
        time.sleep(0.1)  # Small delay for processing

    processing = False

# speed for Gcode must be in mm/min
# max speed of the printer is 250mm/s => 15000 mm/s 
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
    send_gcode('M400')  # Wait for moves to finish


def get_position():
    """Get the current position from the printer."""
    ser.write(('M114' + '\n').encode())
    position_data = ser.readline().decode().strip()

    while "X" not in position_data:
        # print(f"Not good: position data: {position_data}")
        position_data = ser.readline().decode().strip()
    # Parse position data
    print(f"Position data: {position_data}")
    # Expected format: 'X:10.00 Y:10.00 Z:0.00 E:0.00 Count X:1000 Y:1000 Z:0\nok\n'

    # Split the string at 'Count' to isolate the first set of values
    if 'Count' in position_data:
        position_line = position_data.split('Count')[0].strip()
    else:
        position_line = position_data
    
    position = {}
    for line in position_line.split('\n'):
        if 'X:' in line and 'Y:' in line and 'Z:' in line:
            parts = line.strip().split()
            for part in parts:
                if part.startswith('X:'):
                    position['x'] = float(part[2:])
                elif part.startswith('Y:'):
                    position['y'] = float(part[2:])
                elif part.startswith('Z:'):
                    position['z'] = float(part[2:])
    return position


def wait_for_response():
    while True:
        response = ser.readline().decode(errors='ignore').strip()
        if response:
            print(f"Received: {response}")
            if response.lower() == 'ok':
                break
            elif response.lower().startswith('error'):
                break
        else:
            # If no response, prevent infinite loop
            time.sleep(0.1)


def home_axes(axes=''):
    command = f'G28 {axes}'.strip()
    send_gcode(command)

def move_extruder(e, speed=300):
    send_gcode('M302 S0')  # Allow cold extrusion
    send_gcode('G91')  # Ensure relative positioning
    command = f'G1 E{e} F{speed}'
    send_gcode(command)
    send_gcode('G90')  # Return to absolute positioning if needed

def unscrew(e, speed=300):
    #to do: extruder motor + z axis
    send_gcode('M302 S0')  # Allow cold extrusion
    send_gcode('G91')  # Ensure relative positioning
    command = f'G1 E{e} F{speed}'
    send_gcode(command)
    send_gcode('G90')  # Return to absolute positioning if needed

def set_fan_speed(fan_number, speed):
    """
    Set the speed of the specified fan.

    Parameters:
    - fan_number (int): The fan number 0 -> fan2, .
    - speed (int): Speed value between 0 (off) and 255 (full speed).
    """
    command = f'M106 P{fan_number} S{speed}'
    send_gcode(command)

def stop_fan(fan_number):
    """
    Stop the specified fan.

    Parameters:
    - fan_number (int): The fan number (usually 0 or 1).
    """
    command = f'M107 P{fan_number}'
    send_gcode(command)

def close_connection():
    global ser
    ser.close()

def save_positions(positions, filename='positions.json'):
    with open(filename, 'w') as f:
        json.dump(positions, f, indent=4)
    print(f'Positions saved to {filename}')

def open_json(filename='positions-stage-1.json'):
    with open(filename, 'r') as f:
        data = json.load(f)
        return data