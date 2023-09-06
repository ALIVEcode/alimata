# Implementation based on the implementation in the example code of the pymata 4 library

from typing import Union
from alimata.core.board import Board
from alimata.core.core import PIN_MODE, print_warning, WRITE_MODE
from alimata.actuators.actuator import Actuator
from time import sleep
from enum import Enum


class Lcd_COMMAND(int, Enum):
    # commands
    LCD_CLEARDISPLAY = 0b00000001
    LCD_RETURNHOME = 0b00000010
    LCD_ENTRYMODESET = 0b00000100
    LCD_DISPLAYCONTROL = 0b00001000
    LCD_CURSORSHIFT = 0b00010000
    LCD_FUNCTIONSET = 0b00100000
    LCD_SETCGRAMADDR = 0b01000000
    LCD_SETDDRAMADDR = 0b10000000

    # flags for display entry mode  1|I/D|S
    LCD_ENTRYRIGHT = 0
    LCD_ENTRYLEFT = 0b00000010
    LCD_ENTRYSHIFTINCREMENT = 0b00000001
    LCD_ENTRYSHIFTDECREMENT = 0

    # flags for display on/off control 1|D|C|B
    LCD_DISPLAYON = 0b00000100  # D
    LCD_DISPLAYOFF = 0  # D
    LCD_CURSORON = 0b00000010  # C
    LCD_CURSOROFF = 0  # C
    LCD_BLINKON = 0b00000001  # B
    LCD_BLINKOFF = 0  # B

    # flags for display/cursor shift 1|S/C|R/L|*
    LCD_DISPLAYMOVE = 0b00001000  # S/C
    LCD_CURSORMOVE = 0  # S/C
    LCD_MOVERIGHT = 0b00000100  # R/L
    LCD_MOVELEFT = 0  # R/L

    # flags for function set 1|DL|N|F|*
    LCD_8BITMODE = 0b00010000  # DL
    LCD_4BITMODE = 0  # DL
    LCD_2LINE = 0b00001000  # N
    LCD_1LINE = 0  # N
    LCD_5x10DOTS = 0b00000100  # F
    LCD_5x8DOTS = 0  # F

    # flags for backlight control
    LCD_BACKLIGHT = 0b00001000
    LCD_NOBACKLIGHT = 0


class Lcd4Bit(Actuator):
    """
    A class used to represent a manual Lcd using 4 bits

    Properties
    ----------
    rows : int
        the number of rows of the lcd (Read only)
    cols : int
        the number of cols of the lcd (Read only)
    backlight : bool
        the state of the backlight
    current_row : int
        the current row of the cursor
    current_col : int
        the current column of the cursor
    custom_chars : dict
        the custom characters of the lcd
    
    Methods
    -------
    print(string: str, col: int = None, row: int = None)
        Prints a string on the LCD at the current position (or at the specified position)
    quick_print(ligne1: str, ligne2: str = "", ligne3: str = "", ligne4: str = "")
        Quickly prints 1 to 4 lines on the LCD
    clear()
        Clears the lcd
    home()
        Sets the cursor to the home position
    set_cursor(col, row)
        Sets the cursor to the specified position
    enable_backlight()
        Enables the backlight
    disable_backlight()
        Disables the backlight
    enable_display()
        Enables the display
    disable_display()
        Disables the display
    enable_cursor()
        Enables the cursor
    disable_cursor()
        Disables the cursor
    enable_blink()
        Enables the blink
    disable_blink()
        Disables the blink
    scroll_display_left()
        Scrolls the display to the left
    scroll_display_right()
        Scrolls the display to the right
    left_to_right()
        Sets the text to left to right
    right_to_left()
        Sets the text to right to left
    
    """

    def __init__(self, board: Board, pin_rs: Union[str, int], pin_en: Union[str, int], pin_4: Union[str, int],
                 pin_5: Union[str, int], pin_6: Union[str, int], pin_7: Union[str, int], cols: int, rows: int,
                 dot_size: int = 0):

        # self.__i2c_port = 0
        self.__pins = [pin_rs, pin_en, pin_4, pin_5, pin_6, pin_7]
        super().__init__(board=board, pin=self.__pins, type_=PIN_MODE.LCD4BIT)

        # Constant values
        # self.__address = adress
        self.__rows = rows
        self.__cols = cols
        self.__dot_size = dot_size

        # Variables
        self.__current_row = 0
        self.__current_col = 0
        self.__custom_chars = {0: [0], 1: [0], 2: [0], 3: [0], 4: [0], 5: [0], 6: [0], 7: [0]}
        self.__writing = False
        self.__current_text = ["", "", "", ""]

        self.__backlight = Lcd_COMMAND.LCD_NOBACKLIGHT
        self.__display_function = Lcd_COMMAND.LCD_4BITMODE | Lcd_COMMAND.LCD_1LINE | Lcd_COMMAND.LCD_5x8DOTS
        self.__display_mode = Lcd_COMMAND.LCD_ENTRYLEFT | Lcd_COMMAND.LCD_ENTRYSHIFTDECREMENT
        self.__display_control = Lcd_COMMAND.LCD_DISPLAYCONTROL | Lcd_COMMAND.LCD_DISPLAYON | Lcd_COMMAND.LCD_CURSOROFF | Lcd_COMMAND.LCD_BLINKOFF

        self.start()

    def start(self):

        if self.__rows >= 1:
            self.__display_function = self.__display_function | Lcd_COMMAND.LCD_2LINE

        if self.__dot_size != 0 and self.__rows == 1:
            self.__display_function = self.__display_function | Lcd_COMMAND.LCD_5x10DOTS

        sleep(0.05)

        # TODO IMPLEMENT THIS
        # self.__i2c_write(self.__backlight)
        sleep(1)

        # put the LCD into 4 bit mode
        self.__send(0b110000, 0, True)
        sleep(0.045)

        self.__send(0b110000, 0, True)
        sleep(0.15)

        self.__send(0b110000, 0, True)
        sleep(0.045)

        self.__send(0b100000, 0, True)

        # set # lines, font size, etc.

        self.__command(Lcd_COMMAND.LCD_FUNCTIONSET | self.__display_function)

        self.__display_control = Lcd_COMMAND.LCD_DISPLAYON | Lcd_COMMAND.LCD_CURSOROFF | Lcd_COMMAND.LCD_BLINKOFF
        self.enable_display()

        self.clear()

        self.__display_mode = Lcd_COMMAND.LCD_ENTRYLEFT | Lcd_COMMAND.LCD_ENTRYSHIFTDECREMENT
        self.__command(Lcd_COMMAND.LCD_ENTRYMODESET | self.__display_mode)

        self.home()

        self.enable_backlight()

        sleep(2)  # wait for the lcd to be ready

        print("LCD 4 bit started")

    @property
    def rows_number(self):
        '''Returns the number of rows'''
        return self.__rows

    @property
    def cols_number(self):
        '''Returns the number of columns of the LCD'''
        return self.__cols

    @property
    def current_row(self):
        '''Returns the current row'''
        return self.__current_row

    @property
    def current_col(self):
        '''Returns the current column'''
        return self.__current_col

    @property
    def backlight(self):
        '''Get or set the backlight state'''
        if self.__backlight == Lcd_COMMAND.LCD_BACKLIGHT:
            return True
        else:
            return False

    @backlight.setter
    def backlight(self, value: bool):
        if value:
            self.enable_backlight()
        else:
            self.disable_backlight()

    @property
    def get_chars(self):
        '''Returns the custom chars'''
        return self.__custom_chars

    @property
    def get_current_text(self):
        '''Returns the current text on the LCD (as a list)'''
        return self.__current_text

    def print(self, string: str, col: Union[int, None] = None, row: Union[int, None] = None):
        '''Prints a string on the LCD at the current position (or at the specified position)'''
        if col is not None and row is not None:
            self.set_cursor(col, row)
        if self.__text_already_set(string, self.current_col, self.current_row):
            print_warning("Text already set on the LCD | skipping ...")
            return
        if self.__writing:
            self.__writing = False
            print_warning("LCD print overwriten")
            sleep(0.1)

        self.__writing = True
        for character in string:
            if not self.__writing:
                break
            self.__send(ord(character), 1)

            # Increment the current column
            self.__current_col += 1
            if self.__current_col == self.__cols:  # If the current column is out of range go to the next line
                self.__current_col = 0
                self.__current_row += 1
                if self.__current_row == self.__rows:  # If the current row is out of range go to the first line
                    self.__current_row = 0

            sleep(0.000002)
        else:
            sleep(0.00005)
        sleep(0.0001)
        self.__writing = False

    def quick_print(self, ligne1: str, ligne2: str = "", ligne3: str = "", ligne4: str = ""):
        '''Quickly prints 1 to 4 lines on the LCD'''
        self.home()
        self.print(ligne1, 0, 0)
        self.print(ligne2, 0, 1)
        self.print(ligne3, 0, 2)
        self.print(ligne4, 0, 3)

    def clear(self):
        '''Clears the LCD'''
        self.__writing = False
        self.__command(Lcd_COMMAND.LCD_CLEARDISPLAY)
        sleep(0.005)

    def home(self):
        '''Sets the cursor to the home position'''
        self.__command(Lcd_COMMAND.LCD_RETURNHOME)

        self.__current_col = 0
        self.__current_row = 0

        sleep(0.002)

    def set_cursor(self, column: int, row: int):
        '''Sets the cursor to a specific position (column, row)'''
        if column == self.__current_col and row == self.__current_row:
            print_warning("Cursor already set to this position | skipping ...")
            return

        row_offsets = [0x00, 0x40, 0x14, 0x54]
        if row > self.__rows:
            row = self.__rows - 1
        self.__command(Lcd_COMMAND.LCD_SETDDRAMADDR | (column + row_offsets[row]))

        self.__current_col = column
        self.__current_row = row

    def disable_display(self):
        '''Disables the display'''
        self.__display_control = self.__display_control & ~ Lcd_COMMAND.LCD_DISPLAYON
        self.__command(Lcd_COMMAND.LCD_DISPLAYON | self.__display_control)

    def enable_display(self):
        '''Enables the display'''
        self.__display_control = self.__display_control | Lcd_COMMAND.LCD_DISPLAYON
        self.__command(Lcd_COMMAND.LCD_DISPLAYCONTROL | self.__display_control)

    def disable_cursor(self):
        '''Disables the cursor'''
        self.__display_control = self.__display_control & ~ Lcd_COMMAND.LCD_CURSORON
        self.__command(Lcd_COMMAND.LCD_DISPLAYCONTROL | self.__display_control)

    def enable_cursor(self):
        '''Enables the cursor'''
        self.__display_control = self.__display_control | Lcd_COMMAND.LCD_CURSORON
        self.__command(Lcd_COMMAND.LCD_DISPLAYCONTROL | self.__display_control)

    def disable_blink(self):
        '''Disables the blinking cursor'''
        self.__display_control = self.__display_control & ~ Lcd_COMMAND.LCD_BLINKON
        self.__command(Lcd_COMMAND.LCD_DISPLAYCONTROL | self.__display_control)

    def enable_blink(self):
        '''Enables the blinking cursor'''
        self.__display_control = self.__display_control | Lcd_COMMAND.LCD_BLINKON
        self.__command(Lcd_COMMAND.LCD_DISPLAYCONTROL | self.__display_control)

    def scroll_display_left(self):
        '''Scrolls the display to the left'''
        self.__command(Lcd_COMMAND.LCD_CURSORSHIFT | Lcd_COMMAND.LCD_DISPLAYMOVE | Lcd_COMMAND.LCD_MOVELEFT)

    def scroll_display_right(self):
        '''Scrolls the display to the right'''
        self.__command(Lcd_COMMAND.LCD_CURSORSHIFT | Lcd_COMMAND.LCD_DISPLAYMOVE | Lcd_COMMAND.LCD_MOVERIGHT)

    def left_to_right(self):
        '''Sets the text direction to left to right'''
        self.__display_mode = self.__display_mode | Lcd_COMMAND.LCD_ENTRYLEFT
        self.__command(Lcd_COMMAND.LCD_ENTRYMODESET | self.__display_mode)

    def right_to_left(self):
        '''Sets the text direction to right to left'''
        self.__display_mode = self.__display_mode & ~ Lcd_COMMAND.LCD_ENTRYLEFT
        self.__command(Lcd_COMMAND.LCD_ENTRYMODESET | self.__display_mode)

    def enable_auto_scroll(self):
        '''Enables automatic scrolling'''
        self.__display_mode = self.__display_mode | Lcd_COMMAND.LCD_ENTRYSHIFTINCREMENT
        self.__command(Lcd_COMMAND.LCD_ENTRYMODESET | self.__display_mode)

    def disable_auto_scroll(self):
        '''Disables automatic scrolling'''
        self.__display_mode = self.__display_mode & ~ Lcd_COMMAND.LCD_ENTRYSHIFTINCREMENT
        self.__command(Lcd_COMMAND.LCD_ENTRYMODESET | self.__display_mode)

    def disable_backlight(self):
        '''Disables the backlight'''
        self.__backlight = Lcd_COMMAND.LCD_NOBACKLIGHT
        # TODO IMPLEMENT THIS
        # self.__i2c_write(0)

    def enable_backlight(self):
        '''Enables the backlight'''
        self.__backlight = Lcd_COMMAND.LCD_BACKLIGHT
        # TODO IMPLEMENT THIS
        # self.__i2c_write(0)

    def creat_char(self, id: int, charmap: list):
        '''Creates a custom character (id 0-7, charmap 8 bytes)'''
        if id < 0 or id > 7:
            raise ValueError('id must be between 0 and 7')
        elif self.__custom_chars[id] != [0]:
            print_warning('Overwriting custom character with id {}'.format(id))

        self.__custom_chars[id] = charmap

        id %= 8

        self.__command(Lcd_COMMAND.LCD_SETCGRAMADDR | (id << 3))

        sleep(0.00005)

        for i in charmap:
            self.__send(i, 1)

        self.set_cursor(0, 0)  # Set cursor to home position

        sleep(0.00005)

        self.set_cursor(self.__current_col, self.__current_row)  # Set cursor to previous position

    def print_char(self, id: int):
        '''Prints a custom character (id 0-7)'''
        if id > 7 or id < 0:
            raise ValueError('id must be between 0 and 7')
        elif self.__custom_chars[id] == [0]:
            raise ValueError(
                'Custom character with id {} does not exist, creat a new char with the creat_char() function'.format(
                    id))
        else:
            self.__send(id, 1)

    def __text_already_set(self, text: str, col: int, row: int) -> bool:
        '''Checks if the text is already on the display'''

        current_text = self.__current_text[row]

        if col != 0:
            if col < len(current_text) and self.__current_text:
                current_text = current_text[col:]  # Remove the text before the col
        if col + len(text) < len(self.__current_text[row]):
            current_text = current_text[:(col + len(text))]  # Get only the text of the lengh

        if text == current_text:
            return True  # the text is already set

        self.__current_text[row] = self.__current_text[row][:col] + text + self.__current_text[row][(col + len(text)):]
        return False

    def __command(self, value):
        self.__send(value, 0)
        sleep(0.000001)

    def __send(self, value: int, mode: int, init: bool = False):
        '''Sends a value to the LCD mode (0, 1 = regerister select)'''

        # extract each pin value and separate it in high and low bits for 4 bit mode
        high_pin7 = (value & 0b10000000) >> 7
        high_pin6 = (value & 0b01000000) >> 6
        high_pin5 = (value & 0b00100000) >> 5
        high_pin4 = (value & 0b00010000) >> 4
        low_pin7 = (value & 0b00001000) >> 3
        low_pin6 = (value & 0b00000100) >> 2
        low_pin5 = (value & 0b00000010) >> 1
        low_pin4 = (value & 0b00000001)

        self.__write_all_pins(high_pin4, high_pin5, high_pin6, high_pin7)
        self.board.write_to_pin(self.__pins[0], WRITE_MODE.DIGITAL, mode)
        self.board.write_to_pin(self.__pins[1], WRITE_MODE.DIGITAL, 1)

        sleep(0.000001)
        self.board.write_to_pin(self.__pins[1], WRITE_MODE.DIGITAL, 0)

        sleep(0.00001)
        if not init:  # init only need half bits

            sleep(0.00004)

            self.__write_all_pins(low_pin4, low_pin5, low_pin6, low_pin7)
            self.board.write_to_pin(self.__pins[1], WRITE_MODE.DIGITAL, 1)
            sleep(0.000001)
            self.board.write_to_pin(self.__pins[1], WRITE_MODE.DIGITAL, 0)

    def __write_all_pins(self, p4: int, p5: int, p6: int, p7: int):
        self.board.write_to_pin(self.__pins[2], WRITE_MODE.DIGITAL, p4)
        self.board.write_to_pin(self.__pins[3], WRITE_MODE.DIGITAL, p5)
        self.board.write_to_pin(self.__pins[4], WRITE_MODE.DIGITAL, p6)
        self.board.write_to_pin(self.__pins[5], WRITE_MODE.DIGITAL, p7)
