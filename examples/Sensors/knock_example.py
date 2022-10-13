from alimata.sensors.knock import Knock
from alimata.core.board import Board
import asyncio

# Defining the pin of the knock sensor (the other pin is connected to ground or 5v)
pin = 2

# Creating a new board
board = Board()


# Only called when the knock sensor is triggered
def callback_function(data):
    print(data[2])


# Creating a new knock object
knock = Knock(board, pin, callback=callback_function)


# Main function
async def setup():
    print("Starting main")


async def loop():
    await asyncio.sleep(1)


board.start(setup, loop)
