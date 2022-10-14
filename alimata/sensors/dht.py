from alimata.core.core import DHT_SENSOR_TYPE, is_async_function, PIN_MODE
from alimata.sensors.sensor import Sensor
from alimata.core.board import Board
import asyncio


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

        Sensor.__init__(self, board=board, pin=pin, callback=callback, type=PIN_MODE.DHT, sensor_type=DHT_SENSOR_TYPE.DHT11)


    @property
    def data(self):
        """Return the Temperature and Humidity ( [ humidity, temperature] )"""
        return self._Sensor__data

    @property
    def temperature(self):
        """Return the Temperature in Celsius (float)"""
        return self._Sensor__data[1]
    
    @property
    def humidity(self): 
        """Return the Humidity in % (float)"""
        return self._Sensor__data[0]

    


    async def _Sensor__is_changed_callback(self, data):
        """Callback when the sensor's data has changed enough"""
        print('henlo')
        try:
            if self.board.is_started:
                self._Sensor__data = [data[4], data[5]]
                if self._Sensor__callback is not None:
                    if is_async_function(self._Sensor__callback):
                        await self._Sensor__callback(self)
                    else:
                        self._Sensor__callback(self)
        except Exception as e:
            print(e)
