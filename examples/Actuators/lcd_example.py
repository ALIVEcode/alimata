from alimata.core.board import Board
from alimata.actuators.lcd import Lcd

board = Board()

lcd = Lcd(board=board, adress=0x27, rows=4, cols=20)
print("Done")
def setup():
    print("Hello World")
    lcd.print("Hello World")
    lcd.set_cursor(0, 1)
    lcd.print("Hello World2")
    lcd.enable_blink()
    lcd.enable_cursor()
    lcd.set_cursor(0, 2)
    pass

def loop():
    pass

board.start(setup, loop)