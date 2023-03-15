from alimata.core.core import PIN_MODE
from alimata.sensors.sensor import Sensor
from alimata.core.board import Board
from typing import Callable, Union, List


class Motion(Sensor):
    """
    A class used to represent a Motion Sensor

    Attributes
    ----------
    pin : str or int
        the data pin of the sensor

    Properties
    ----------
    data : bool
        the value of the Motion sensor (Mouvment (True) or No mouvment (False))
    """

    def __init__(self, board: Board, pin: Union[str, int],
                 on_change: Union[Callable[[List[Union[float, int]]], None], None] = None):

        # Initialises the motion sensor as no mouvment
        self.__state = False  # PRIVATE

        super().__init__(board=board, pin=pin, type_=PIN_MODE.DIGITAL_INPUT, on_change=on_change)

    # ABSTRACT FROM SENSOR
    @property
    def data(self) -> bool:
        """Return the current status of the motion sensor (True or False)"""
        return self.__state

    # ABSTRACT FROM SENSOR
    # Change the status of the motion when motion is detected
    # Back end callback function (*not user defined*)
    def _update_data(self, data: list):
        if data[2] == 1:
            self.__state = True
        else:
            self.__state = False
