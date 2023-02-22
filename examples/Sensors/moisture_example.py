from alimata.sensors.moisture import Moisture
from alimata.core.board import Board
from time import sleep

#Defining the pin of the moisture sensor
pin = "A0"

#Creating a new board
board = Board()

#Only called when the moisture is changed
def callback_function(obj):
    print("value : " + str(obj.level))

#Creating a new moisture sensor object
moisture = Moisture(board, pin, on_change=callback_function)

#Main function
def setup():
    print("Starting main")

def loop():
    print(moisture.level)
    sleep(1)


board.start(setup, loop)