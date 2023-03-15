from alimata.core.core import PIN_MODE
from alimata.sensors.sensor import Sensor
from alimata.core.board import Board
from typing import Callable, Union, List


class Button(Sensor):
    """
    A class used to represent a Button

    Attributes
    ----------
    pin : str
        the pin of the Button
    invert : bool
        if the button is inverted or not

    Properties
    ----------
    data : bool
        the value of the Button (Pressed (True) or Released (False))
    """

    def __init__(self, board: Board, pin: Union[int, str], invert: bool = False,
                 on_change: Union[Callable[[List[Union[float, int]]], None], None] = None):
        # Initialises the button as not pressed
        self.__state = False  # PRIVATE

        # Initialises the invert value
        self.invert = invert  # PUBLIC

        super().__init__(board=board, pin=pin, type_=PIN_MODE.PULLUP, on_change=on_change)

    # ABSTRACT FROM SENSOR
    @property
    def data(self) -> bool:
        """Return the current status of the button (True or False)"""
        return self.__state

    # ABSTRACT FROM SENSOR
    # Change the status of the button when pressed
    # Back end callback function (*not user defined*)
    def _update_data(self, data: list):
        self.__state = not data[2] if self.invert else data[2] == 1
