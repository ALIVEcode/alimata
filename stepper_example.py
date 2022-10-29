import asyncio
from alimata.core.board import Board
from alimata.actuators.stepper import Stepper
from time import sleep

# Create a board object
board = Board()

#Set the pin of the servo


# Create a servo object
stepper = Stepper(board=board, pin1=9, pin2=6, pin3=5, pin4=3, steps_per_revolution=2048)

#Main function
def setup():
    print("Starting main")
    
    print("Doing 1 revolution")
    stepper.step(2048)
    sleep(stepper.speed + 1)

    print("Doing 1 revolution but faster")
    stepper.speed = 10
    stepper.step(2048)
    sleep(stepper.speed  + 1)

def loop():
    pass


board.start(setup, loop)