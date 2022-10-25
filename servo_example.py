import asyncio
from alimata.core.board import Board
from alimata.actuators.servo import Servo
from asyncio import sleep

# Create a board object
board = Board()

#Set the pin of the servo
servo_pin = 3

# Create a servo object
servo = Servo(board=board, pin_=servo_pin)

#Main function
async def setup():
    print("Starting main")
    print("Setting servo to 0")
    servo.data = 0

async def loop():
    if servo.runing:
        return
    else:
        print("Moving to 90")
        servo.data = 90
        await sleep(1)
        print("Moving to 0")
        servo.data = 0
        await sleep(1)
        print("Moving to 180")
        servo.data = 180
        await sleep(1)
        print("Slowly moving to 0")
        servo.move_to(0, 2000)


board.start(setup, loop)