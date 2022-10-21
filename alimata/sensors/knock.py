from alimata.core.core import is_async_function, PIN_MODE
from alimata.core.board import Board
from alimata.sensors.sensor import Sensor


class Knock(Sensor):
    """
    A class used to represent a Knock Sensor
    
    Attributes
    ----------
    data : Int
        the value of the Knock Sensor (0-1023)
    pin : str
        the pin of the Knock Sensor
    """

    def __init__(self, board: Board, pin, callback=None):
        
        Sensor.__init__(self, board=board, pin=pin, callback=callback, type=PIN_MODE.PULLUP)

        self.__treshold = 0

    
    @property
    def data(self):
        """Return the current status of the knock sensor (True or False)"""
        return self._Sensor__data

    @proprety
    def treshold(self):
        return self.__treshold

    @treshold.setter
    def setTreshold(self, treshold: int):
        self.__treshold = treshold
        self.board.write_to_pin(self.pin, PIN_MODE.PWM, treshold)

    # Change the status of the sensor is knock
    async def _Sensor__is_changed_callback(self, data):
        """Callback when the knock sensor value has changed"""
        try:
            if self.board.is_started:
                self._Sensor__data = data
                if Sensor.is_ready(self) and self._Sensor__callback is not None:
                    if is_async_function(self._Sensor__callback):
                        await self._Sensor__callback(self)
                    else:
                        self._Sensor__callback(self)
        except Exception as e:
            print(e)


