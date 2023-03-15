from alimata.core.board import Board
from alimata.core.core import PIN_MODE, SPI_COMMAND, print_warning
from alimata.actuators.actuator import Actuator
from typing import Union
from enum import Enum


class MATRIX_COMMAND(int, Enum):
    NO_OP = 0x00
    DECODE = 0x09
    INTENSITY = 0x0A
    SCAN_LIMIT = 0x0B
    SHUTDOWN = 0x0C
    DISPLAY_TEST = 0x0F


# The 16 bits sent to the MAX7219 are: (X means don't care)
# 15 14 13 12 11 10  9  8 7  6  5  4  3  2  1  0
# X  X  X  X  A3 A2 A1 A0 D7 D6 D5 D4 D3 D2 D1 D0
# MATRIX_COMMAND = A0, A1, A2, A3

class Matrix(Actuator):

    def __init__(self, board: Board, cs_pin: Union[int, str], row: int, column: int):
        self.__cs_pin = cs_pin
        super().__init__(pin=[cs_pin], board=board, type_=PIN_MODE.SPI)

        self.__intensity = 15

        # Set the scan limit
        self.__row = row
        self.__column = column

        if column > 8:
            raise ValueError("Column must be between 1 and 8")
        data = [MATRIX_COMMAND.SCAN_LIMIT, column]
        self.board.spi_communication(cs_pin=cs_pin, command=SPI_COMMAND.WRITE_BLOCKING, _bytes=data)

        # Set decode mode to 0
        data = [MATRIX_COMMAND.DECODE, 0x00]
        self.board.spi_communication(cs_pin=cs_pin, command=SPI_COMMAND.WRITE_BLOCKING, _bytes=data)

        # set display test to 0
        data = [MATRIX_COMMAND.DISPLAY_TEST, 0x00]
        self.board.spi_communication(cs_pin=cs_pin, command=SPI_COMMAND.WRITE_BLOCKING, _bytes=data)

        # set shutdown to 1
        data = [MATRIX_COMMAND.SHUTDOWN, 0x01]
        self.board.spi_communication(cs_pin=cs_pin, command=SPI_COMMAND.WRITE_BLOCKING, _bytes=data)

        # set intensity
        self.intensity = self.__intensity

    def draw(self, col: int, row: int, value: int):
        if col > self.__column + 1:
            raise ValueError("Column must be between 1 and {}".format(self.__column))
        if row > self.__row + 1:
            raise ValueError("Row must be between 1 and {}".format(self.__row))
        if value > 1:
            raise ValueError("Value must be 0 or 1")

        data = [col, value << row]
        self.board.spi_communication(cs_pin=self.__cs_pin, command=SPI_COMMAND.WRITE_BLOCKING, _bytes=data)

    def draw_map(self, map: list):
        '''Draw a map on the display [[0,0],[1,0] ...]'''
        # TODO
        raise NotImplementedError("draw map is not implemented")

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
        self.board.spi_communication(cs_pin=self.__cs_pin, command=SPI_COMMAND.WRITE_BLOCKING, _bytes=data)

    def clear(self):
        '''Clear the display'''
        for i in range(0, self.__column + 1):
            self.draw(i, 0, 0)
