from alimata.sensors.luminosity import Luminosity
from alimata.core.board import Board
from time import sleep

#Defining the pin of the luminosity sensor
pin = "A0"

#Creating a new board
board = Board()

#Only called when the luminosity is changed
def callback_function(obj):
    print("value : " + str(obj.data))

#Creating a new luminosity sensor object
luminosity = Luminosity(board, pin, on_change=callback_function)

#Main function
def setup():
    print("Starting main")

def loop():
    print(luminosity.data)
    sleep(1)


board.start(setup, loop)