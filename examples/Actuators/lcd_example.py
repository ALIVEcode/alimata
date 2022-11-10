from alimata.core.board import Board
from alimata.actuators.lcd import Lcd
from time import sleep

board = Board()

char = [  
    0b00100,
    0b01110,
    0b11111,
    0b11111,
    0b01110,
    0b00100,
    0b01110,
    0b11111
]

lcd = Lcd(board=board, adress=0x27, rows=4, cols=20)

def setup():
    lcd.print("    Hello World")
    lcd.set_cursor(0, 1)
    lcd.print("abcdefghijklmnopqrst")
    lcd.enable_blink()
    lcd.enable_cursor()
    lcd.creat_char(0, char)
    lcd.set_cursor(0, 2)
    lcd.print_char(0)
    lcd.set_cursor(1, 3)
    lcd.print("Waiting 5 seconds")
    
    sleep(5)

    lcd.clear()
    lcd.quick_print("Hello World 1", "Hello World 2", "Hello World 3", "Hello World 4")

def loop():
    pass

board.start(setup, loop)