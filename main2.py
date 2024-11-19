import time
from functions.indexV2 import (
    initialize_port,
    send_gcode,
    move_to_position,
    home_axes,
    move_extruder,
    close_connection,
)

initialize_port()

# Wake up the printer
send_gcode('M17')  # Enable steppers

# Homing
home_axes()

# Go up to absolute position Z=50
move_to_position(z=50)

# Define positions
positions = {
    'A': {'x': 50, 'y': 50, 'z': 20},
    'B': {'x': 150, 'y': 50, 'z': 20},
    'C': {'x': 150, 'y': 150, 'z': 20},
    'D': {'x': 50, 'y': 150, 'z': 20},
}

for pos_name in ['A', 'B', 'C', 'D']:
    # Move to position at Z=50
    move_to_position(
        x=positions[pos_name]['x'],
        y=positions[pos_name]['y'],
        z=50
    )

    # Go down to specified Z
    move_to_position(z=positions[pos_name]['z'])

    # Wait for 1 second
    time.sleep(1)

    # Extrude filament
    move_extruder(5, speed=300)  # Extrude 5mm of filament

    # Wait for 1 second
    time.sleep(1)

    # Go back up to Z=50
    move_to_position(z=50)

close_connection()
