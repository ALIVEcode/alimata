from alimata.sensors.button import Button
from alimata.actuators.led import Led
from alimata.core.board import Board
from asyncio import sleep, all_tasks


#Creating a new board
board = Board()


#Only called when the button is pressed or released
def callback_function(btn):
    print("Function 1 | PIN : " + str(btn.pin) + " | Value : " + str(btn.data))

    if(btn.data):
        led.intensity = 255
        led.on()
    else:
        led.off()

def callback2(btn):
    print("Function 2 | PIN : " + str(btn.pin) + " | Value : " + str(btn.data))
    if(btn.data):
        led.intensity = 100
        led.on()
    else:
        led.off()
    

buttonPin = 2
buttonPin2 = 6
ledPin = 3

button2 = Button(board, 2, on_change=callback_function, invert=True)
button = Button(board, 6, on_change=callback2, invert=True)
led = Led(board, ledPin)


#Main function
async def setup():
    print("Starting main")


async def loop():
    await sleep(1)
    # print(button.data)


board.start(setup, loop)