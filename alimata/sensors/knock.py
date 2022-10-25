import time
from alimata.core.core import PIN_MODE
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

    def __init__(self, board: Board, pin: str, treshold: int = 10 ,on_change: Callable[[list[float | int]], None] | None = None):
        
        self.__value = 0
        self.__is_knocked = False
        self.__treshold = 0
        self.__last_knocked = time.time()
        super().__init__(board=board, pin=pin, on_change=on_change, type_=PIN_MODE.ANALOG_INPUT)

    


    @property
    def data(self):
        """Return the current status of the knock sensor (True or False)"""
        return self.__value

    # Change the status of the sensor is knock
    async def _update_data(self, py_data: list):
        """Callback when the knock sensor value has changed"""
        print(time.time() - self.__last_knocked)
        if py_data[2] >= self.__treshold and (time.time() - self.__last_knocked) * 1000 > 100:
            self.__is_knocked = True
            self.__last_knocked = time.time()
            self.__value = py_data[2]

