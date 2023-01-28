from alimata.core.board import Board
from alimata.actuators.lcd4bit import Lcd4Bit
from time import sleep

board = Board()

lcd = Lcd4Bit(board=board, pin_rs=8, pin_en=9, pin_4=4, pin_5=5, pin_6=6, pin_7=7, rows=2, cols=16)

def setup():
    lcd.print("Hello World")
    lcd.set_cursor(0, 1)
    lcd.print("abcdefghijklmnopqrst")
    lcd.enable_blink()
    lcd.enable_cursor()
    # lcd.creat_char(0, char)
    # lcd.set_cursor(0, 2)
    # lcd.print_char(0)
    lcd.set_cursor(1, 1)
    lcd.print("Waiting 5 seconds")
    
    for i in range(5):
        lcd.set_cursor(0, 1)
        lcd.print("Waiting {} seconds".format(5-i))
        sleep(1)

    print("Clearing")
    lcd.clear()
    # lcd.quick_print("Hello World 1", "Hello World 2", "Hello World 3", "Hello World 4")


def loop():
    pass

board.start(setup, loop)