from alimata.sensors.sonar import Sonar
from alimata.core.board import Board
import asyncio

# Defining the pins of the HC-SR04 sonar
triger_pin = 10
echo_pin = 9

# Creating a new board
board = Board()

# Creating a new sonar object
sonar = Sonar(board, triger_pin, echo_pin)


# Main function
async def setup():
    print("Starting main")


async def loop():
    print(sonar.get_distance())
    await asyncio.sleep(1)


board.start(setup, loop)
