import time
from functions.indexV2 import (
    initialize_port,
    send_gcode,
    move_to_position,
    home_axes,
    close_connection,
    set_fan_speed,
    stop_fan,
    unscrew
)

# Costants
x_offset = 0
y_offset = 0
z_offset = 0

x_box = 0
y_box = 0

z_fast = 50
max_speed = 15000
speed = 10000
z_speed = 300

# Define mouse positions
positions = {
    'A': {'x': x_offset+0.5, 'y': y_offset+8, 'z': z_offset},
    'B': {'x': x_offset+3.95, 'y': y_offset+8, 'z': z_offset},
    'C': {'x': x_offset+4.45, 'y': y_offset+1.9, 'z': z_offset},
    'D': {'x': x_offset+3.45, 'y': y_offset+0, 'z': z_offset},
    'E': {'x': x_offset+1, 'y': y_offset+0, 'z': z_offset},
    'F': {'x': x_offset+0, 'y': y_offset+1.9, 'z': z_offset},
}  



initialize_port()

set_fan_speed(fan_number=0, speed=255)
time.sleep(1)

# Wake up the printer
send_gcode('M17')  # Enable steppers

# Homing
print("Homing ...")
home_axes() 

set_fan_speed(fan_number=0, speed=255)

# Go up to navigation position
move_to_position(z=z_fast)
print("Start disassembling Superlight Pro 2")
time.sleep(1)


for pos_name in ['A', 'B', 'C', 'D', 'E', 'F']:
    print(f"Position: {pos_name}")
    
    # Move to position 
    move_to_position(
        x=positions[pos_name]['x'],
        y=positions[pos_name]['y'],
        z=z_fast,
        speed=speed
    )

    # Go down to specified Z
    move_to_position(z=positions[pos_name]['z'])

    # Magnetize endpoint

    # Unscrew
    time.sleep(1)
    # to do: relationship between speed and rotation
    unscrew(5, speed=z_speed)  
    time.sleep(1)

    # Go back up to Z fast
    move_to_position(z=z_fast)

    # Move to the screw box
    move_to_position(
        x=x_box,
        y=y_box,
        z=z_fast,
        speed=speed
    )

    # Demagnetize endpoint


stop_fan(fan_number=0)
close_connection()
