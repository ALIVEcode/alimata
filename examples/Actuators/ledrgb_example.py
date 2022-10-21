from alimata.actuators.ledRGB import LedRGB
from alimata.core.board import Board
from asyncio import sleep
import random


# Defining the pin of the led
redPin = 9
greenPin = 10
bluePin = 11

# Creating a new board
board = Board()

# Creating a new led object
rgbled = LedRGB(board, redPin, greenPin, bluePin)


# Main function
async def setup():
    print("Starting main")
    rgbled.rgb = (255, 255, 255)
    rgbled.on()


async def loop():
    
    # get random rgb values
    rgbled.rgb = (50, 0, 0)
    await sleep(0.1)
    rgbled.rgb = (0, 50, 0)
    await sleep(0.1)
    rgbled.rgb = (0, 0, 50)
    await sleep(0.1)
    

board.start(setup, loop)
