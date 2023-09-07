from alimata.core.core import STEPPER_TYPE
from alimata.core.board import Board
from alimata.actuators.stepper import Stepper
from time import sleep

# Create a board object
board = Board()

# Set the pin of the servo


# Create a servo object
stepper = Stepper(board=board, stepper_type=STEPPER_TYPE.FULL4WIRE, pin1=8, pin2=10, pin3=9, pin4=11)

def callback(data):
    print(data)
    exit()

# Main function
def setup():
    print("Starting main")

    print("Doing 1 revolution")
    stepper.speed = 450
    stepper.move(2048, blocking=False, callback=callback)
    print(f"Current position : {stepper.current_position} | Remaining distance : {stepper.distance_to_go}")
    print("waiting 5 second")
    sleep(5) 
    print(f"Current position : {stepper.current_position} | Remaining distance : {stepper.distance_to_go}")

def loop():
    pass


board.start(setup, loop)
