#Implementation based on the implementation in the example code of the pymata 4 library

from alimata.core.board import Board
from alimata.core.core import PIN_MODE, I2C_COMMAND, print_warning
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
    LCD_DISPLAYON = 0b00000100 #D
    LCD_DISPLAYOFF = 0 #D
    LCD_CURSORON = 0b00000010 #C
    LCD_CURSOROFF = 0 #C
    LCD_BLINKON = 0b00000001 #B
    LCD_BLINKOFF = 0 #B

    # flags for display/cursor shift 1|S/C|R/L|*
    LCD_DISPLAYMOVE = 0b00001000 #S/C
    LCD_CURSORMOVE = 0 #S/C
    LCD_MOVERIGHT = 0b00000100 # R/L
    LCD_MOVELEFT = 0 #R/L

    # flags for function set 1|DL|N|F|*
    LCD_8BITMODE = 0b00010000 #DL
    LCD_4BITMODE = 0 #DL
    LCD_2LINE = 0b00001000 #N
    LCD_1LINE = 0 #N
    LCD_5x10DOTS = 0b00000100 #F
    LCD_5x8DOTS = 0 #F

    # flags for backlight control
    LCD_BACKLIGHT = 0b00001000
    LCD_NOBACKLIGHT = 0

    EN = 0b00000100 # Enable bit
    RW = 0b00000010 # Read/Write bit
    RS = 0b00000001 # Register select bit

class Lcd(Actuator):
    """
    A class used to represent a i2c Lcd

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
    

    def __init__(self, board: Board, adress, cols: int, rows: int, dot_size: int = 0):

        self.__read_delay = 0
        super().__init__(board=board, pin=self.__read_delay, type_=PIN_MODE.I2C)

        self.__board = board

        # Constant values
        self.__address = adress
        self.__rows = rows
        self.__cols = cols
        self.__dot_size = dot_size

        # Variables
        self.__current_row = 0
        self.__current_col = 0
        self.__custom_chars = {0: None, 1: None, 2: None, 3: None, 4: None, 5: None, 6: None, 7: None}

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

        self.__i2c_write(self.__backlight)
        sleep(1)

        # put the LCD into 4 bit mode
        self.__write_4_bits(0b110000)
        sleep(0.0045)

        self.__write_4_bits(0b110000)
        sleep(0.0045)

        self.__write_4_bits(0b110000)
        sleep(0.00015)

        self.__write_4_bits(0b100000)

        # set # lines, font size, etc.

        self.__command(Lcd_COMMAND.LCD_FUNCTIONSET | self.__display_function)

        self.__display_control = Lcd_COMMAND.LCD_DISPLAYON | Lcd_COMMAND.LCD_CURSOROFF | Lcd_COMMAND.LCD_BLINKOFF
        self.enable_display()

        self.clear()

        self.__display_mode = Lcd_COMMAND.LCD_ENTRYLEFT | Lcd_COMMAND.LCD_ENTRYSHIFTDECREMENT
        self.__command(Lcd_COMMAND.LCD_ENTRYMODESET | self.__display_mode)

        self.home()

        self.enable_backlight()

        print("LCD started | adress : " + hex(self.__address))
    
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
    def address(self):
        '''Returns the address of the LCD'''
        return self.__address
    
    @property
    def backlight(self):
        '''Get or set the backlight state'''
        if self.__backlight == Lcd_COMMAND.LCD_BACKLIGHT:
            return True
        else:
            return False
    
    @property
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
    
    def print(self, string: str):
        '''Prints a string on the LCD'''
        for character in string:
            self.__send(ord(character), Lcd_COMMAND.RS)
            sleep(0.000002)
        else:
            sleep(0.00005)
        sleep(0.0001)

    def clear(self):
        '''Clears the LCD'''
        self.__command(Lcd_COMMAND.LCD_CLEARDISPLAY)
        sleep(0.002)

    def home(self):
        '''Sets the cursor to the home position'''
        self.__command(Lcd_COMMAND.LCD_RETURNHOME)

        self.__current_col = 0
        self.__current_row = 0
        
        sleep(0.002)

    def set_cursor(self, column: int, row: int):
        '''Sets the cursor to a specific position (column, row)'''
        row_offsets = [0x00, 0x40, 0x14, 0x54]
        if row > self.__rows:
            row = self.__rows - 1
        self.__command(Lcd_COMMAND.LCD_SETDDRAMADDR | (column + row_offsets[row]))

        self.__current_col = column
        self.__current_row = row

    def disable_display(self):
        '''Disables the display'''
        self.__display_control = self.__display_control &~ Lcd_COMMAND.LCD_DISPLAYON
        self.__command(Lcd_COMMAND.LCD_DISPLAYON | self.__display_control)

    def enable_display(self):
        '''Enables the display'''
        self.__display_control = self.__display_control | Lcd_COMMAND.LCD_DISPLAYON
        self.__command(Lcd_COMMAND.LCD_DISPLAYCONTROL | self.__display_control)

    def disable_cursor(self):
        '''Disables the cursor'''
        self.__display_control = self.__display_control &~ Lcd_COMMAND.LCD_CURSORON
        self.__command(Lcd_COMMAND.LCD_DISPLAYCONTROL | self.__display_control)

    def enable_cursor(self):
        '''Enables the cursor'''
        self.__display_control = self.__display_control | Lcd_COMMAND.LCD_CURSORON
        self.__command(Lcd_COMMAND.LCD_DISPLAYCONTROL | self.__display_control)

    def disable_blink(self):
        '''Disables the blinking cursor'''
        self.__display_control = self.__display_control &~ Lcd_COMMAND.LCD_BLINKON
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
        self.__display_mode = self.__display_mode &~ Lcd_COMMAND.LCD_ENTRYLEFT
        self.__command(Lcd_COMMAND.LCD_ENTRYMODESET | Lcd_COMMAND.__display_mode)

    def enable_auto_scroll(self):
        '''Enables automatic scrolling'''
        self.__display_mode = self.__display_mode | Lcd_COMMAND.LCD_ENTRYSHIFTINCREMENT
        self.__command(Lcd_COMMAND.LCD_ENTRYMODESET | self.__display_mode)

    def disable_auto_scroll(self):
        '''Disables automatic scrolling'''
        self.__display_mode = self.__display_mode &~ Lcd_COMMAND.LCD_ENTRYSHIFTINCREMENT
        self.__command(Lcd_COMMAND.LCD_ENTRYMODESET | self.__display_mode)

    def disable_backlight(self):
        '''Disables the backlight'''
        self.__backlight = Lcd_COMMAND.LCD_NOBACKLIGHT
        self.__i2c_write(0)

    def enable_backlight(self):
        '''Enables the backlight'''
        self.__backlight = Lcd_COMMAND.LCD_BACKLIGHT
        self.__i2c_write(0)
    
    def creat_char(self, id: int, charmap: list):
        '''Creates a custom character (id 0-7, charmap 8 bytes)'''
        if id < 0 or id > 7:
            raise ValueError('id must be between 0 and 7')
        elif self.__custom_chars[id] is not None:
            print_warning('Overwriting custom character with id {}'.format(id))
        
        self.__custom_chars[id] = charmap

        id %= 8

        self.__command(Lcd_COMMAND.LCD_SETCGRAMADDR | (id << 3))

        sleep(0.00005)

        for i in charmap:
            self.__send(i, Lcd_COMMAND.RS)
        
        self.set_cursor(0, 0) # Set cursor to home position

        sleep(0.00005)

        self.set_cursor(self.__current_col, self.__current_row) # Set cursor to previous position
    
    def print_char(self, id: int):
        '''Prints a custom character (id 0-7)'''
        if id > 7 or id < 0:
            raise ValueError('id must be between 0 and 7')
        elif self.__custom_chars[id] is None:
            raise ValueError('Custom character with id {} does not exist, creat a new char with the creat_char() function'.format(id))
        else:
            self.__write_4_bits(Lcd_COMMAND.RS | (id & 0xF0))
            self.__write_4_bits(Lcd_COMMAND.RS | ((id << 4) & 0xF0))

    def __command(self, value):
        self.__send(value, 0)
        sleep(0.00005)

    def __send(self, value: int, mode: int):
        high_bits: int = value & 0b11110000
        low_bits: int = (value << 4) & 0b11110000
        self.__write_4_bits(high_bits | mode)
        self.__write_4_bits(low_bits | mode)

    def __write_4_bits(self, value: int):
        self.__i2c_write(value)
        self.__pulse_enable(value)

    def __pulse_enable(self, data: int):
        self.__i2c_write(data | Lcd_COMMAND.EN)
        sleep(0.000001)

        self.__i2c_write(data &~ Lcd_COMMAND.EN)
        sleep(0.00005)

    def __i2c_write(self, data: int):
        self.__board.i2c_comunication(I2C_COMMAND.WRITE, self.address, args=[data | self.__backlight])
