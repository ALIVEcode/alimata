from alimata.sensors.button import Button
from alimata.actuators.led import Led
from alimata.core.board import Board
from asyncio import sleep, all_tasks


#Creating a new board
board = Board()


#Only called when the button is pressed or released
def callback_function(btn):
    print("pressed | PIN : " + str(btn.pin) + " | Value : " + str(btn.value))

    if(btn.value):
        led.on()
    else:
        led.off()

def callback2(btn):
    print("callback2")
    pass

buttonPin = 2
buttonPin2 = 6
ledPin = 5

button2 = Button(board, 2, callback=callback_function)
button = Button(board, 6, callback=callback_function)
led = Led(board, ledPin)


#Main function
async def setup():
    print("Starting main")


async def loop():
    await sleep(1)


board.start(setup, loop)