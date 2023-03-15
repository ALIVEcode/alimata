from alimata.sensors.motion import Motion
from alimata.core.board import Board
from time import sleep

# Defining the pin of the motion sensor
pin = 2

# Creating a new board
board = Board()


# Only called when there is a change in the motion sensor
def callback_function(obj):
    print("movement : " + str(obj.data))


# Creating a new motion sensor object
motion = Motion(board, pin, on_change=callback_function)


# Main function
def setup():
    print("Starting main")


def loop():
    print(motion.data)
    sleep(1)


board.start(setup, loop)
