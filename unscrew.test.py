import time
from functions.arduino import move_servo
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

x_box = 0
y_box = 0

z_fast = 10
# max_speed = 15000
max_speed = 10000
speed = 10000
z_speed = 300
speed_unscrew = 20


# Define mouse positions
positions = open_json("data/positions-stage-1.json")


def main():
    initialize_port()

    set_fan_speed(fan_number=0, speed=255)
    time.sleep(1)

    # Wake up the printer
    send_gcode('M17')  # Enable steppers

    # Homing
    print("Homing ...")
    # home_axes()

    set_fan_speed(fan_number=0, speed=255)

    # Go up to navigation position
    # move_to_position(z=z_fast)
    print("Start disassembling Superlight Pro 2")
    time.sleep(1)

    move_servo(180)

    for pos_name in ['A']:
        print(f"Position: {pos_name}")

        # Move to position
        # move_to_position(
        #     x=positions[pos_name]['x'],
        #     y=positions[pos_name]['y'],
        #     z=z_fast,
        #     speed=speed
        # )

        # # Go down to specified Z
        # move_to_position(z=positions[pos_name]['z'])

        # Magnetize endpoint
        time.sleep(2)
        move_servo(180)
        time.sleep(2)

        # Unscrew
        time.sleep(1)
        unscrew(10, speed=speed_unscrew)
        time.sleep(10)

        
        # move_to_position(z=10)

        # Go back up to Z fast
        move_to_position(z=z_fast)

        # Move to the screw box
        # move_to_position(
        #     x=x_box,
        #     y=y_box,
        #     z=z_fast,
        #     speed=speed
        # )

        # move_to_position(
        #     x=50,
        #     y=50,
        #     z=z_fast,
        #     speed=speed
        # )

        # Demagnetize endpoint
        time.sleep(2)
        move_servo(0)
        time.sleep(2)


    stop_fan(fan_number=0)
    close_connection()


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
    position_labels = ['A', 'B', 'C', 'D', 'E', 'F']


    for idx, label in enumerate(position_labels):
        input(f"Press 'Enter' to record position {label}...")
        # Wait a moment to ensure printer is ready
        time.sleep(0.5)
        position = get_position()
        if position:
            positions[label] = position
            print(f"Position {label}: {position}")
        else:
            print(f"Failed to get position {label}")
            return


    print("Recorded positions:")
    print(positions)
    save_positions(positions, "data/positions-stage-1-v2.json")
    close_connection()


main()
# get_superlight_position()