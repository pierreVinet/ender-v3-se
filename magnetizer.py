from functions.arduino import move_servo
import time

def main():
    move_servo(90)
    time.sleep(2)
    move_servo(0)
    time.sleep(2)
    move_servo(180)
    time.sleep(2)
    move_servo(90)

main