from alimata.core.board import Board
from alimata.core.core import PIN_MODE, SPI_COMMAND, print_warning
from alimata.actuators.actuator import Actuator
from typing import Union, Enum

class MATRIX_COMMAND(int, Enum):
    NO_OP = 0x00
    DIGIT0 = 0x01
    DIGIT1 = 0x02
    DIGIT2 = 0x03
    DIGIT3 = 0x04
    DIGIT4 = 0x05
    DIGIT5 = 0x06
    DIGIT6 = 0x07
    DIGIT7 = 0x08
    DECODE = 0x09
    INTENSITY = 0x0A
    SCAN_LIMIT = 0x0B
    SHUTDOWN = 0x0C
    DISPLAY_TEST = 0x0F
#15 14 13 12 11 10  9  8 7  6  5  4  3  2  1  0 
#X  X  X  X  A3 A2 A1 A0 D7 D6 D5 D4 D3 D2 D1 D0
#MATRIX_COMMAND = A0, A1, A2, A3

class Matrix(Actuator):

    def __init__(self, board: Board, cs_pin: Union[int, str], row: int, column: int):
        self.__cs_pin = cs_pin
        super().__init__(pin=[cs_pin], board=board, type_=PIN_MODE.SPI)

        self.__intensity = 15

        # Set the scan limit
        self.__row = row
        self.__column = column

        if column + 1 > 8:
            raise ValueError("Column must be between 1 and 8")
        data = [MATRIX_COMMAND.SCAN_LIMIT, column]
        self.board.spi_commuinication(cs_pin=cs_pin, command=SPI_COMMAND.WRITE_BLOCKING, bytes=data)

        #Set decode mode to 0
        data = [MATRIX_COMMAND.DECODE, 0x00]
        self.board.spi_commuinication(cs_pin=cs_pin, command=SPI_COMMAND.WRITE_BLOCKING, bytes=data)

        #set display test to 0
        data = [MATRIX_COMMAND.DISPLAY_TEST, 0x00]
        self.board.spi_commuinication(cs_pin=cs_pin, command=SPI_COMMAND.WRITE_BLOCKING, bytes=data)

    def draw(self, col: int, row: int, value: int):
        if col > self.__column + 1:
            raise ValueError("Column must be between 1 and {}".format(self.__column))
        if row > self.__row + 1:
            raise ValueError("Row must be between 1 and {}".format(self.__row))
        if value > 1:
            raise ValueError("Value must be 0 or 1")
        
        if col == 1:
            data = [MATRIX_COMMAND.DIGIT0, value << row]
        elif col == 2:
            data = [MATRIX_COMMAND.DIGIT1, value << row]
        elif col == 3:
            data = [MATRIX_COMMAND.DIGIT2, value << row]
        elif col == 4:
            data = [MATRIX_COMMAND.DIGIT3, value << row]
        elif col == 5:
            data = [MATRIX_COMMAND.DIGIT4, value << row]
        elif col == 6:
            data = [MATRIX_COMMAND.DIGIT5, value << row]
        elif col == 7:
            data = [MATRIX_COMMAND.DIGIT6, value << row]
        elif col == 8:
            data = [MATRIX_COMMAND.DIGIT7, value << row]
        self.board.spi_commuinication(cs_pin=self.__cs_pin, command=SPI_COMMAND.WRITE_BLOCKING, bytes=data)


    @property
    def intensity(self) -> int:
        '''Get or set the intensity of the display (0-15)'''
        return self.__intensity
    
    @intensity.setter
    def intensity(self, value: int):
        if value > 15:
            print_warning("Intensity > 15, setting to 15")
            value = 15
        self.__intensity = value
        data = [MATRIX_COMMAND.INTENSITY, value]
        self.board.spi_commuinication(cs_pin=self.__cs_pin, command=SPI_COMMAND.WRITE_BLOCKING, bytes=data)
