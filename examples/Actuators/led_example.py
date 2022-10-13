from alimata.actuators.led import Led
from alimata.sensors.button import Button
from alimata.core.board import Board
import asyncio

# Defining the pin of the button (the other pin is connected to ground or 5v)
button_pin = 2
# Defining the pin of the led
led_pin = 3

# Creating a new board
board = Board()

# Creating a new led object
led = Led(board, led_pin)


# Creating a new button object
async def callback_function(data):
    await led.toggle()  # Toggle on the led when the button is pressed


button = Button(board, button_pin, callback=callback_function)


# Main function
async def setup():
    print("Starting main")


async def loop():
    await asyncio.sleep(1)


board.start(setup, loop)
