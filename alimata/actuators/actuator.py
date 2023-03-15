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
                 stepper_type: STEPPER_TYPE = None):
        ''' Returns None exept for the stepper'''
        # Create Public Attributes
        self.board = board
        self.pin = pin

        # Create Private Attributes
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
