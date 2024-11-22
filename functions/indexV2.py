import serial
import time

ser = None  # Global variable to hold the serial connection
processing = False

def initialize_port():
    global ser
    # Replace 'COM7' with your serial port (e.g., '/dev/ttyUSB0' for Linux)
    ser = serial.Serial('COM9', 115200, timeout=1)
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


def get_current_position():
    send_gcode('M114')  # Get current position
    response = ser.readline().decode().strip()
    print(f"Current Position: {response}")
    return response

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

def close_connection():
    global ser
    ser.close()
