from alimata.core.core import PIN_MODE
from alimata.core.board import Board
from alimata.sensors.sensor import Sensor
from typing import Callable, Union, List


class Sonar(Sensor):
    """
    A class used to represent a Sonar

    Attributes
    ----------
    distance_in_cm : float
        the distance of the sensor in cm
    distance_in_inch : float
        the distance of the sensor in inches
    data : float
        the distance of the sensor in cm

    Methods
    -------
    is_ready()
        Return True if the sensor is ready to be used
        
    """

    def __init__(self, board: Board, trigger_pin: Union[str, int], echo_pin: Union[str, int],
                 on_change: Union[Callable[[List[Union[float, int]]], None], None] = None):

        pin_ = [trigger_pin, echo_pin]

        super().__init__(board=board, pin=pin_, on_change=on_change, type_=PIN_MODE.SONAR)

        self.__data = -1

    @property
    def data(self):
        """Return the current distance of the sensor"""
        return self.__data
    
    @property
    def distance_in_cm(self):
        """Return the current distance of the sensor"""
        return self.__data
    
    @property
    def distance_in_inch(self):
        """Return the current distance of the sensor in inch"""
        return self.__data / 2.54

    def _update_data(self, data):
        """Callback when the sensor's data has changed enough"""
        self.__data = data[2]


