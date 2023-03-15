from alimata.core.core import STEPPER_TYPE
from alimata.core.board import Board
from alimata.actuators.stepper import Stepper
from time import sleep

# Create a board object
board = Board()

# Set the pin of the servo


# Create a servo object
stepper = Stepper(board=board, stepper_type=STEPPER_TYPE.FULL4WIRE, pin1=9, pin2=5, pin3=6, pin4=3)


# Main function
def setup():
    print("Starting main")

    print("Doing 1 revolution")
    stepper.speed = 1000
    stepper.move(2048)
    sleep(60)  # wait for 1 full rotation at that speed and 1 second


def loop():
    pass


board.start(setup, loop)
