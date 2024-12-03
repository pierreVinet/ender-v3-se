from functions.arduino import move_servo
import time

def main():
    time.sleep(2)
    # move_servo(0)
    move_servo(180)

main()