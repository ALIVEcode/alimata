from alimata.core.core import DHT_SENSOR_TYPE, PIN_MODE
from alimata.sensors.sensor import Sensor
from alimata.core.board import Board
from typing import Callable, Union, List


class DHT(Sensor):
    """
    A class used to represent a Button

    Attributes
    ----------
    temperature : float
        the temperature of the sensor in Celsius
    humidity : float
        the humidity of the sensor in %
    data : [humidity, temperature]
        the data of the DHT sensor
    pin : str
        the pin of the Button

    Methods
    -------
    is_ready()
        Return True if the sensor is ready to be used
        
    """

    def __init__(self, board: Board, pin: str, on_change: Union[Callable[[List[Union[float, int]]], None], None ]= None):

        super().__init__(board=board, pin=pin, type_=PIN_MODE.DHT, on_change=on_change)


        # self.__data is a tuple of (humidity, temperature)
        self.__data = None 


    @property
    def data(self):
        """Return the Temperature and Humidity (humidity, temperature)"""
        return self.__data

    @property
    def temperature(self) -> float:
        """Return the Temperature in Celsius (float)"""
        return self.__data[1]
    
    @property
    def humidity(self): 
        """Return the Humidity in % (float)"""
        return self.__data[0]

    


    # Back end callback function (*not user defined*)
    def _update_data(self, data):
        """Callback when the sensor's data has changed enough"""
        self.__data = (data[4], data[5])
