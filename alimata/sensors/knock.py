from alimata.core.core import is_async_function, PIN_MODE
from alimata.core.board import Board
from alimata.sensors.sensor import Sensor


class Knock(Sensor):
    """
    A class used to represent a Knock Sensor
    
    Attributes
    ----------
    data : bool
        the value of the Knock Sensor (True or False)
    invert : bool
        if the sensor is inverted or not
    pin : str
        the pin of the Knock Sensor
    """

    def __init__(self, board: Board, pin, invert: bool = False, callback=None):
        
        Sensor.__init__(self, board=board, pin=pin, callback=callback, type=PIN_MODE.PULLUP)

        self.invert = invert
    
    @property
    def data(self):
        """Return the current status of the knock sensor (True or False)"""
        return self._Sensor__data

    # Change the status of the sensor is knock
    async def _Sensor__is_changed_callback(self, data):
        """Callback when the knock sensor value has changed"""
        try:
            if self.board.is_started:
                if self.invert:
                    self._Sensor__data = not bool(data[2])
                else:
                    self._Sensor__data = bool(data[2])
                
                if Sensor.is_ready(self) and self._Sensor__callback is not None:
                    if is_async_function(self._Sensor__callback):
                        await self._Sensor__callback(self)
                    else:
                        self._Sensor__callback(self)
        except Exception as e:
            print(e)


