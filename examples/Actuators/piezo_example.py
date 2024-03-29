from alimata.actuators.piezo import Piezo
from alimata.core.board import Board
from time import sleep

# Defining the pin of the led
piezo_pin = 3

# Creating a new board
board = Board()

# Creating a new led object
piezo = Piezo(board, piezo_pin)


# Main function
def setup():
    print("Starting main")


def loop():
    sleep(1)
    piezo.play_tone(1000, 1000)
    sleep(2)
    piezo.play_tone(5000)
    sleep(0.5)
    piezo.stop_tone()


board.start(setup, loop)
