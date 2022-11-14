import asyncio
from alimata.core.board import Board
from alimata.actuators.stepper import Stepper
from time import sleep

raise NotImplementedError("Stepper not implemented yet")

# Create a board object
board = Board()

#Set the pin of the servo


# Create a servo object
stepper = Stepper(board=board, pin1=9, pin2=5, pin3=6, pin4=3, steps_per_revolution=2048)

#Main function
def setup():
    print("Starting main")
    
    print("Doing 1 revolution")
    stepper.step(2048)
    sleep(60 / stepper.speed + 1) # wait for 1 full rotation at that speed and 1 second

    print("Doing 1 revolution but faster")
    stepper.speed = 17
    stepper.step(2048)
    sleep(60 / stepper.speed  + 1) # wait for 1 full rotation at that speed and 1 second

    print("Doing 1 revolution but in reverse")
    stepper.speed = 10
    stepper.step(-2048)
    sleep(60 / stepper.speed + 1) # wait for 1 full rotation at that speed and 1 second

def loop():
    pass


board.start(setup, loop)