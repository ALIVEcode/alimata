from alimata.sensors.button import Button
from alimata.core.board import Board
import asyncio

#Defining the pin of the button sensor (the other pin is connected to ground or 5v)
pin = 2

#Creating a new board
board = Board()

#Only called when the button is pressed or released
def callback_function(data):
    print(data[2])

#Creating a new button object
button = Button(board, pin, callback=callback_function)

#Main function
async def setup():
    print("Starting main")

async def loop():
    await asyncio.sleep(1)


board.start(setup, loop)