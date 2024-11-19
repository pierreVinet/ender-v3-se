import serial
import time

ser = None  # Global variable to hold the serial connection

def initialize_port():
    global ser
    # Replace 'COM7' with your serial port (e.g., '/dev/ttyUSB0' for Linux)
    ser = serial.Serial('COM7', 115200, timeout=1)
    time.sleep(2)  # Wait for the connection to initialize

def send_gcode(command, wait_for_completion=False):
    ser.write((command + '\n').encode())
    print(f"Sent: {command}")
    wait_for_response()  # Wait for 'ok' after sending the command

    if wait_for_completion:
        # Wait until all movements are completed
        ser.write(('M400\n').encode())
        print("Sent: M400")
        wait_for_response()  # Wait for 'ok' after M400

def send_gcode2(command, wait_for_completion=False):
    ser.write((command + '\n').encode())
    print(f"Sent: {command}")
    wait_for_response2()  # Wait for 'ok' after sending the command


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

def wait_for_response2():
    while True:
        response = ser.readline().decode(errors='ignore').strip()
        if response:
            print(f"Received: {response}")
            # if response.lower() == 'ok':
            #     break
            # elif response.lower().startswith('error'):
            #     break
        else:
            # If no response, prevent infinite loop
            time.sleep(0.1)

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
    send_gcode2(command, wait_for_completion=True)

def home_axes(axes=''):
    command = f'G28 {axes}'.strip()
    send_gcode(command, wait_for_completion=True)

def move_extruder(e, speed=300):
    send_gcode('M302 S0')  # Allow cold extrusion
    send_gcode('G91')  # Ensure relative positioning
    command = f'G1 E{e} F{speed}'
    send_gcode(command, wait_for_completion=True)
    send_gcode('G90')  # Return to absolute positioning if needed

def close_connection():
    global ser
    ser.close()
