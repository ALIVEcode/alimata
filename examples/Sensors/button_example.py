from alimata.sensors.button import Button
from alimata.core.board import Board
from asyncio import sleep

#Defining the pin of the button sensor (the other pin is connected to ground or 5v)
pin = 2

#Creating a new board
board = Board()

#Only called when the button is pressed or released
def callback_function(data):
    print("pressed" + str(data.data))

#Creating a new button object
button = Button(board, pin, on_change=callback_function, invert=True)

#Main function
async def setup():
    print("Starting main")

async def loop():
    # print(button.value)
    print(button.data)
    await sleep(1)


board.start(setup, loop)