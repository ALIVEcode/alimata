from alimata.core.core import DHT_SENSOR_TYPE, PIN_MODE
from alimata.sensors.sensor import Sensor
from alimata.core.board import Board


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

    def __init__(self, board: Board, pin: str, callback=None):

        Sensor.__init__(self, board=board, pin=pin, type_=PIN_MODE.DHT)


        # self.__data is a tuple of (humidity, temperature)
        self.__data = None 

        # Initialises the Callback function that is *user defined*
        self.__callback = callback


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
    async def _update_data(self, data):
        """Callback when the sensor's data has changed enough"""
        try:
            self.__data = (data[4], data[5])
            if Sensor.is_ready(self) and self.__callback is not None:
                self.__callback(self)
        except Exception as e:
            print(e)
