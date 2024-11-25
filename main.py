import time
from functions.indexV2 import (
    initialize_port,
    send_gcode,
    move_to_position,
    home_axes,
    move_extruder,
    close_connection,
    set_fan_speed,
    stop_fan
)

initialize_port()


set_fan_speed(fan_number=0, speed=255)
time.sleep(2)
# set_fan_speed(fan_number=1, speed=255)
# time.sleep(2)
# Wake up the printer
send_gcode('M17')  # Enable steppers

# Homing
home_axes() 

set_fan_speed(fan_number=0, speed=255)

print("Starting to move to positions")
# Go up to absolute position Z=50
move_to_position(z=20, speed=15000)

time.sleep(1)


# Define positions
positions = {
    'A': {'x': 0, 'y': 0, 'z': 20},
    'B': {'x': 220, 'y': 00, 'z': 20},
    'C': {'x': 220, 'y': 220, 'z': 20},
    'D': {'x': 0, 'y': 220, 'z': 20},
}

for pos_name in ['A', 'B', 'C', 'D']:
    # Move to position at Z=50
    move_to_position(
        x=positions[pos_name]['x'],
        y=positions[pos_name]['y'],
        z=50,
        speed=15000
    )

    # Go down to specified Z
    # move_to_position(z=positions[pos_name]['z'])

    # Wait for 1 second
    time.sleep(1)

    # Extrude filament
    move_extruder(5, speed=300)  # Extrude 5mm of filament

    # Wait for 1 second
    time.sleep(1)

    # Go back up to Z=50
    # move_to_position(z=50)


stop_fan(fan_number=0)
close_connection()
