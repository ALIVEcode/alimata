from alimata.actuators.ledRGB import LedRGB
from alimata.core.board import Board
from time import sleep


# Defining the pin of the led
redPin = 9
greenPin = 10
bluePin = 11

# Creating a new board
board = Board()

# Creating a new led object
rgb_led = LedRGB(board, redPin, greenPin, bluePin)


# Main function
def setup():
    print("Starting main")
    rgb_led.rgb = (255, 255, 255)
    rgb_led.on()


def loop():
    
    # get random rgb values
    rgb_led.rgb = (50, 0, 0)
    sleep(0.1)
    rgb_led.rgb = (0, 50, 0)
    sleep(0.1)
    rgb_led.rgb = (0, 0, 50)
    sleep(0.1)
    

board.start(setup, loop)
