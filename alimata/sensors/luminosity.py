from alimata.core.core import PIN_MODE, map_range
from alimata.sensors.sensor import Sensor
from alimata.core.board import Board
from typing import Callable, Union, List


class Luminosity(Sensor):
    """
    A class used to represent a Luminosity Sensor

    Attributes
    ----------
    pin : str
        the signal analog pin of the sensor

    Methods
    ---------
    mapped_data(min, max) : int
        Return the current value of the light intensity mapped to the given range (min to max)

    Properties
    ----------
    data : int
        the current light intensity (0 to 255)
    """

    def __init__(self, board: Board, pin: str,
                 on_change: Union[Callable[[List[Union[float, int]]], None], None] = None):
        super().__init__(board=board, pin=pin, type_=PIN_MODE.ANALOG_INPUT, on_change=on_change)

        self.__data: int = -1

    def mapped_data(self, min_val: int, max_val: int) -> int:
        """Return the current value of the light intensity mapped to the given range (min to max)"""
        return int(map_range(self.__data, 0, 255, min_val, max_val))

    # ABSTRACT FROM SENSOR
    @property
    def data(self) -> int:
        """Return the current light intensity (0 to 255)"""
        return self.__data

    # ABSTRACT FROM SENSOR
    # Change the status of the luminosity when the luminoosty change
    # Back end callback function (*not user defined*)
    def _update_data(self, data: list):
        self.__data = data[2]
