from alimata.sensors.button import Button
from alimata.core.board import Board
from time import sleep

# Creating a new board
board = Board()


# Only called when the button2 is pressed or released
def callback_function(obj):
    print("The value of %d the pin is now %d" % (obj.data[1], obj.data[2]))


# Creating a new buttons object
button1 = Button(board, 2)
button2 = Button(board, 3, on_change=callback_function)


# Setup function
def setup():
    print("Setup function")
    sleep(1)
    print("Loop function is gona start")


# Loop function
# Print a and b every second
async def loop():
    print("a")
    sleep(1)
    print("b")
    sleep(1)


board.start(setup, loop)
