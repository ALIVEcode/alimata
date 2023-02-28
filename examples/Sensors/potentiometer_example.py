from alimata.sensors.potentiometer import Potentiometer
from alimata.core.board import Board
from time import sleep

# Defining the pin of the potentiometer sensor
pin = "A0"

# Creating a new board
board = Board()


# Only called when the potentiometer is moved
def callback_function(obj):
    print("value : " + str(obj.data))


# Creating a new Potentiometer object
potentiometer = Potentiometer(board, pin, on_change=callback_function)


# Main function
def setup():
    print("Starting main")


def loop():
    print(potentiometer.data)
    sleep(1)


board.start(setup, loop)
