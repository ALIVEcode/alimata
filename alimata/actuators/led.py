from alimata.core.board import Board
from alimata.core.core import PIN_MODE, WRITE_MODE
from alimata.actuators.actuator import Actuator
from typing import Union


class Led(Actuator):
    """
    A class used to represent a Led

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
        super().__init__(board=board, pin=pin, type_=PIN_MODE.ANALOG_OUTPUT)

        # Initialises the led to off
        self.__data = False

        # Initialises the intensity to 255
        self.__intensity = 255

    def toggle(self):
        """
        Toggle the led on or off \n
        """
        if self.__data:
            self.off()
        else:
            self.on()

    def on(self):
        """
        Turn the led on \n
        """
        self.__data = True  # Set the status of the led to on
        self.board.write_to_pin(self.pin, WRITE_MODE.ANALOG, self.__intensity)  # Set the intensity of the led
        # await self.board.write_to_pin(self.pin, WRITE_MODE.PWM, 255)

    def off(self):
        """
        Turn the led off \n
        """
        self.__data = False  # Set the status of the led to off
        self.board.write_to_pin(self.pin, WRITE_MODE.ANALOG, 0)

    @property
    def intensity(self):
        """
        Get or Set the intensity of the led [0-255]\n
        """
        return self.__intensity

    @intensity.setter
    def intensity(self, intensity: int):
        """
        Set the intensity of the led [0-255]\n
        """
        self.__intensity = intensity
        self.board.write_to_pin(self.pin, WRITE_MODE.ANALOG, intensity)

    @property
    def data(self):
        """
        Get or Set the current status of the led [True/False]\n
        """
        return self.__data

    @data.setter
    def data(self, status: bool):
        if status:
            self.on()
        else:
            self.off()
