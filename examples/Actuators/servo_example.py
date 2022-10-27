import asyncio
from alimata.core.board import Board
from alimata.actuators.servo import Servo
from time import sleep

# Create a board object
board = Board()

#Set the pin of the servo
servo_pin = 3

# Create a servo object
servo = Servo(board=board, pin_=servo_pin)

#Main function
def setup():
    print("Starting main")
    print("Setting servo to 0")
    servo.data = 0

def loop():
    if servo.runing:
        return
    else:
        print("Moving to 180")
        servo.move_to(180)
        sleep(1)
        print("Moving to 90")
        servo.move_to(90)
        sleep(1)
        print("Moving to 135")
        servo.move_to(135)
        sleep(1)
        print("Moving to 45 in 2 seconds")
        servo.move_to(45, 2000)
        sleep(1)


board.start(setup, loop)