from alimata.sensors.button import Button
from alimata.actuators.led import Led
from alimata.core.board import Board
from asyncio import sleep, all_tasks


#Creating a new board
board = Board()


#Only called when the button is pressed or released
async def callback_function(btn):
    print("pressed")
    print(btn.pin) # True if pressed and False if released
    # led.on()

    # if(btn.value):
        # led.on()
    # else:
        # led.off()
def callback2():
    pass

buttonPin = 2
ledPin = 5

button = Button(board, buttonPin, callback=callback_function)
button2 = Button(board, 6, callback=callback_function)
led = Led(board, ledPin)


#Main function
async def setup():
    print("Starting main")
    led.on()


async def loop():
    print(len(list(all_tasks())))
    # print(all_tasks())
    await sleep(1)


board.start(setup, loop)