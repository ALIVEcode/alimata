from alimata.sensors.knock import Knock
from alimata.core.board import Board
import asyncio

# Defining the pin of the knock sensor (the other pin is connected to ground or 5v)
pin = "10"

# Creating a new board
board = Board()


# Only called when the knock sensor is triggered
def knocked(knock : Knock):
    # print(knock.data)
    if knock.data == True:
        print("Ding!")

# Creating a new knock object
knock = Knock(board, pin, on_change=knocked)


# Main function
async def setup():
    print("Starting main")


async def loop():
    await asyncio.sleep(1)
    


board.start(setup, loop)
