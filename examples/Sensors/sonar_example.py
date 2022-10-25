from alimata.sensors.sonar import Sonar
from alimata.core.board import Board
from time import sleep

# Defining the pins of the HC-SR04 sonar
triger_pin = 10
echo_pin = 9

# Creating a new board
board = Board()

# Creating a new sonar object
sonar = Sonar(board, triger_pin, echo_pin)


# Main function
def setup():
    print("Starting main")


def loop():
    print(sonar.get_distance())
    sleep(1)


board.start(setup, loop)
