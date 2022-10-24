from alimata.core.core import is_async_function, PIN_MODE
from alimata.core.board import Board
from alimata.sensors.sensor import Sensor
from typing import Callable


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

    def __init__(self, board: Board, pin: str, on_change: Callable[[list[float | int]], None] | None = None):
        
        self.__state = False
        super().__init__(board=board, pin=pin, on_change=on_change, type_=PIN_MODE.ANALOG)

    
    @property
    def data(self):
        """Return the current status of the knock sensor (True or False)"""
        return self.__state

    # Change the status of the sensor is knock
    async def _update_data(self, data: list):
        """Callback when the knock sensor value has changed"""
        self.__state= bool(data[2])
        


