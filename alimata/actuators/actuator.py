from alimata.core.board import Board
from alimata.core.core import PIN_MODE
from typing import Union

from abc import ABC, abstractmethod

class Actuator(ABC):

   # Constructor of the class Actuator
    def __init__(self, 
    pin: Union[str, int], 
    board: Board,
    type_: PIN_MODE,
    min_pulse: int = 544,
    max_pulse: int = 2400,
    steps_per_revolution: int = None,
    ):

        # Create Public Attributes
        self.board = board
        self.pin = pin

        # Create Private Attributes
        self.__type = type_
        self.__min_pulse = min_pulse
        self.__max_pulse = max_pulse
        self.__steps_per_revolution = steps_per_revolution

        # Set the pin and other properties of the actuator
        self.board.set_pin_mode(
            pin=self.pin,
            type_=self.__type,
            min_pulse=self.__min_pulse,
            max_pulse=self.__max_pulse,
            steps_per_revolution=self.__steps_per_revolution)


   
   

    # MUST BE IMPLEMENTED IN THE CHILD CLASS
    @property
    @abstractmethod
    def data(self):
        """Return the data of the actuator"""
        pass

    # MUST BE IMPLEMENTED IN THE CHILD CLASS
    @data.setter
    @abstractmethod
    def data(self, value):
        """Set the data of the actuator"""
        pass