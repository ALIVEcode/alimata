from alimata.actuators.led import Led
from alimata.sensors.button import Button
from alimata.core.board import Board
from asyncio import sleep

# Defining the pin of the led
led_pin = 5

# Creating a new board
board = Board()

# Creating a new led object
led = Led(board, led_pin)


# Main function
async def setup():
    print("Starting main")



async def loop():
    await sleep(1)
    led.on()
    print("on")
    await sleep(1)
    led.off()
    print("off")
    await sleep(1)
    led.on()
    led.intensity = 100
    print("100")
    await sleep(1)
    led.intensity = 255
    print("255")
    await sleep(1)
    led.off()



board.start(setup, loop)
