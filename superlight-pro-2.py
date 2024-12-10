import time
from functions.arduino import close_arduino, move_servo
from functions.creality import (
    initialize_port,
    send_gcode,
    move_to_position,
    home_axes,
    close_connection,
    set_fan_speed,
    stop_fan,
    unscrew,
    get_position,
    save_positions,
    open_json
)

# Costants
x_offset = 0
y_offset = 0
z_offset = 0

x_home = 134.25
y_home = 125.0

x_box = 110
y_box = 220

x_finish = 110
y_finish = 220

z_fast = 46
max_speed = 10000
speed = 10000
z_speed = 300
speed_unscrew = 20


# Define mouse positions
positions = open_json("data/positions-stage-1.json")
# positions = open_json("data/positions-stage-2.json")


def main():
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
    # time.sleep(1)

    # move_servo(180)

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
        move_to_position(z=positions[pos_name]['z'] + 5)

        #wait for user input
        # input(f"Press 'Enter' to procede...")

        # Go down to specified Z
        move_to_position(z=positions[pos_name]['z'])

        # Magnetize endpoint
        # time.sleep(2)
        move_servo(180)
        time.sleep(1)

        # Unscrew
        # time.sleep(1)
        unscrew(1, speed=speed_unscrew*3, elevation=False)
        unscrew(3, speed=speed_unscrew)
        # time.sleep(1)

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
        # time.sleep(2)
        move_servo(0)
        time.sleep(1
                   )

    move_to_position(
        x=x_finish,
        y=y_finish,
        z=z_fast,
        speed=speed
    )

    stop_fan(fan_number=0)
    close_connection()
    close_arduino()


def get_superlight_position():
    initialize_port()

    # Wake up the printer
    send_gcode('M17')  # Enable steppers
    # Homing
    print("Homing ...")
    home_axes() 

    set_fan_speed(fan_number=0, speed=255)

    # Go up to navigation position
    move_to_position(z=32.7)
    time.sleep(1)
    
    positions = {}
    position_labels = ["buffer", 'A', 'B', 'C', 'D', 'E', 'F']
    idx = 0

    while idx < len(position_labels):
        label = position_labels[idx]
        input(f"Press 'Enter' to record position {label}...")
        # Wait a moment to ensure the printer is ready
        time.sleep(0.5)
        position = get_position()

        if position:
            positions[label] = position
            print(f"Position {label}: {position}")
        else:
            print(f"Failed to get position {label}")
            return 
        
        unscrew(3, speed=speed_unscrew)

        # Ask user if the position is correct
        user_input = input("Press 'f' to redo the position or 'Enter' to continue: ").strip().lower()
        if user_input == "f":
            print(f"Redoing position {label}...")
            continue  # Redo the current label
        else:
            idx += 1  # Move to the next label


    print("Recorded positions:")
    print(positions)
    save_positions(positions, "data/positions-stage-2-v2.json")
    close_connection()
    close_arduino()


main()
# get_superlight_position()