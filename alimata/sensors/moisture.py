from alimata.core.core import PIN_MODE, maprange
from alimata.sensors.sensor import Sensor
from alimata.core.board import Board
from typing import Callable, Union, List

class Moisture(Sensor):
    """
    A class used to represent a Moisture Sensor

    Attributes
    ----------
    pin : str
        the signal analog pin of the sensor

    Methods
    ---------
    mapped_data(min, max) : int
        Return the current value of moisture mapped to the given range (min to max)

    level : float
        Return the current level of moisture (0 to 100)

    Properties
    ----------
    data : int
        the current moisture value (0 to 255)
    """

    def __init__(self, board: Board, pin: str, on_change: Union[Callable[[List[Union[float, int]]], None], None ]= None):

        super().__init__(board=board, pin=pin, type_=PIN_MODE.ANALOG_INPUT, on_change=on_change)

        self.__data = None
    
    def mapped_data(self, min: int, max: int) -> int:
        """Return the current value of moisture mapped to the given range (min to max)"""
        return maprange(self.__data, 0, 255, min, max)
    
    def level(self) -> float:
        """Return the current level of moisture (0 to 100)"""
        return maprange(self.__data, 0, 255, 0, 100)

    # ABSTRACT FROM SENSOR
    @property
    def data(self) -> int:
        """Return the current moisture value (0 to 255)"""
        return self.__data


    # ABSTRACT FROM SENSOR
    # Change the status of the luminosity when the luminoosty change
    # Back end callback function (*not user defined*)
    def _update_data(self, data: list):
        self.__data = data[2]


