from alimata.sensors.button import Button
from alimata.core.board import Board
import asyncio

# Creating a new board
board = Board()


# Only called when the button2 is pressed or released
async def callback_function(data):
    print("The value of %d the pin is now %d" % (data[1], data[2]))


# Creating a new buttons object
button1 = Button(board, 2)
button2 = Button(board, 3, on_change=callback_function)


# Setup function
async def setup():
    print("Setup function")
    await asyncio.sleep(1)
    print("Loop function is gona start")


# Loop function
# Print a and b every second
async def loop():
    print("a")
    await asyncio.sleep(1)
    print("b")
    await asyncio.sleep(1)


board.start(setup, loop)
