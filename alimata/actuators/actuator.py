from alimata.core.board import Board
from alimata.core.core import PIN_MODE, STEPPER_TYPE
from typing import Union

from abc import ABC


class Actuator(ABC):

    # Constructor of the class Actuator
    def __init__(self,
                 pin: Union[str, int, list],
                 board: Board,
                 type_: PIN_MODE,
                 min_pulse: int = 544,
                 max_pulse: int = 2400,
                 stepper_type: Union[STEPPER_TYPE, None] = None):
        ''' Returns None exept for the stepper'''


        # Create Private Attributes
        self.__board = board
        self.__pin = pin
        self.__type = type_
        self.__min_pulse = min_pulse
        self.__max_pulse = max_pulse
        self.__stepper_type = stepper_type

        # Set the pin and other properties of the actuator and save the returned id if present
        self.__id = self.board.set_pin_mode(
            pin=self.pin,
            type_=self.__type,
            min_pulse=self.__min_pulse,
            max_pulse=self.__max_pulse,
            stepper_type=self.__stepper_type)

    @property
    def id(self) -> int:
        '''Returns the id of the actuator'''
        return self.__id
    
    @property
    def board(self) -> Board:
        '''Returns the board of the actuator'''
        return self.__board
    
    @property
    def pin(self) -> Union[str, int, list]:
        '''Returns the pin of the actuator'''
        return self.__pin
