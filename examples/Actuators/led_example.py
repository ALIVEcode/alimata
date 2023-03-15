from alimata.actuators.led import Led
from alimata.core.board import Board
from time import sleep

# Defining the pin of the led
led_pin = 5

# Creating a new board
board = Board()

# Creating a new led object
led = Led(board, led_pin)


# Main function
def setup():
    print("Starting main")


def loop():
    sleep(1)
    led.on()
    print("on")
    sleep(1)
    led.off()
    print("off")
    sleep(1)
    led.on()
    led.intensity = 100
    print("100")
    sleep(1)
    led.intensity = 255
    print("255")
    sleep(1)
    led.off()


board.start(setup, loop)
