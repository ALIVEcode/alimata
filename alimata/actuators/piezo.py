from alimata.core.board import Board
from alimata.core.core import PIN_MODE, WRITE_MODE
from alimata.actuators.actuator import Actuator
from typing import Union


class Piezo(Actuator):
    """
    A class used to represent a Piezo

    Properties
    ----------
    data : bool
        the status of the led (on or off)
    intensity : int
        the intensity of the led (0-255)

    Methods
    -------
    toggle()
        Toggle the led on or off
    on()
        Turn the led on
    off()
        Turn the led off
    """

    def __init__(self, board: Board, pin: Union[str, int]):
        super().__init__(board=board, pin=pin, type_=PIN_MODE.TONE)

    def play_tone(self, frequency: int = 1000, duration: int = 0):
        """
        Turn the led on \n
        """

        if duration != 0:
            self.board.write_to_pin(pin=self.pin, type_=WRITE_MODE.TONE, value=frequency, duration=duration)
        else:
            self.board.write_to_pin(pin=self.pin, type_=WRITE_MODE.TONE_CONTINUOUS, value=frequency)

    def stop_tone(self):
        """
        Turn the led off \n
        """
        # self.__data = False # Set the status of the led to off
        self.board.write_to_pin(pin=self.pin, type_=WRITE_MODE.TONE_STOP, value=0)
