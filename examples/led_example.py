from alimata.actuators.led import Led
from alimata.sensors.button import Button
from alimata.core.board import Board
import asyncio

# Defining the pin of the button (the other pin is connected to ground or 5v)
# button_pin = 2
# Defining the pin of the led
led_pin = 5

# Creating a new board
board = Board()

# Creating a new led object
led = Led(board, led_pin)


# Creating a new button object
# async def callback_function(data):
    # await led.toggle()  # Toggle on the led when the button is pressed


# button = Button(board, button_pin, callback=callback_function)


# Main function
async def setup():
    print("Starting main")



async def loop():
    await asyncio.sleep(1)
    led.on()
    print("on")
    await asyncio.sleep(1)
    await led.off()
    print("off")
    await asyncio.sleep(1)
    led.on()
    # await led.intensity = 100
    print("100")
    await asyncio.sleep(1)
    # await led.intensity(255)
    print("255")
    await asyncio.sleep(1)
    await led.off()



board.start(setup, loop)
