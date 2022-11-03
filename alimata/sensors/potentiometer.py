from alimata.core.core import PIN_MODE
from alimata.sensors.sensor import Sensor
from alimata.core.board import Board
from typing import Callable, Union, List


class Potentiometer(Sensor):
    """
    A class used to represent a Potentiometer

    Attributes
    ----------
    pin : str
        analog pin of the Potentiometer
    invert : bool
        if the Potentiometer is inverted or not

    Properties
    ----------
    data : bool
        the value of the Potentiometer (0 to 255)
    """



    def __init__(self, board: Board, pin: str, invert: bool = False, differential: int = 1, on_change: Union[Callable[[List[Union[float, int]]], None], None ]= None):
        

        # Initialises the Potentiometer as 0
        self.__data = 0 # PRIVATE

        # Initialises the invert value
        self.invert = invert # PUBLIC

        super().__init__(board=board, pin=pin, type_=PIN_MODE.ANALOG_INPUT, differential=differential, on_change=on_change)



    # ABSTRACT FROM SENSOR
    @property
    def data(self) -> bool:
        """Return the current value of the Potentiometer (True or False)"""
        return self.__data


    # ABSTRACT FROM SENSOR
    # Change the value of the Potentiometer
    # Back end callback function (*not user defined*)
    def _update_data(self, data: list):
        self.__data = data[2]
