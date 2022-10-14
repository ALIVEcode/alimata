from alimata.actuators.led import Led
from alimata.sensors.button import Button
from alimata.core.board import Board
from asyncio import sleep

# Defining the pin of the button (the other pin is connected to ground or 5v)
# button_pin = 2
# Defining the pin of the led
led_pin = 5

# Creating a new board
board = Board()

# Creating a new led object
led = Led(board, led_pin)

# board.set_pin_mode(led_pin, "PWM")

# led.pin = 6

# board.setpin(led, 6)


# Creating a new button object
# async def callback_function(data):
    # await led.toggle()  # Toggle on the led when the button is pressed


# button = Button(board, button_pin, callback=callback_function)


# Main function
async def setup():
    print("Starting main")



async def loop():
    await sleep(1)
    await led.on()
    print("on")
    await sleep(1)
    await led.off()
    print("off")
    await sleep(1)
    await led.on()
    led.intensity = 100
    print("100")
    await sleep(1)
    led.intensity = 255
    print("255")
    await sleep(1)
    await led.off()



board.start(setup, loop)
