from alimata.actuators.matrix import Matrix
from alimata.core.board import Board
import time

board = Board()

matrix = Matrix(board=board, cs_pin=0, row=8, column=8)

def setup():
    for i in range(8):
        for j in range(8):
            matrix.draw(col=i, row=j, value=1)
            print("i: {}, j: {}".format(i, j))
            time.sleep(0.5)
    
    matrix.intensity = 0
    print("Intensity: {}".format(matrix.intensity))
    time.sleep(1)
    matrix.intensity = 15
    print("Intensity: {}".format(matrix.intensity))
    time.sleep(1)
    matrix.intensity = 6
    print("Intensity: {}".format(matrix.intensity))
    time.sleep(1)
    matrix.intensity = 10
    print("Intensity: {}".format(matrix.intensity))
    time.sleep(1)
    matrix.intensity = 15
    print("Intensity: {}".format(matrix.intensity))

def loop():
    pass

board.start(setup, loop)