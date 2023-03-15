from alimata.actuators.led import Led
from alimata.core.board import Board
from alimata.actuators.actuator import Actuator
from typing import Union


class LedRGB(Actuator):
    """
    A class used to represent a RGB Led

    Properties
    ----------
    data : bool
        the status of the ledrgb (on or off)
    rgb : tuple
        the rgb value of the ledrgb (0-255, 0-255, 0-255)
    red : int
        the red value of the ledrgb (0-255)
    green : int
        the green value of the ledrgb (0-255)
    blue : int
        the blue value of the ledrgb (0-255)

    Methods
    -------
    toggle()
        Toggle the led on or off
    on()
        Turn the led on
    off()
        Turn the led off
    """

    def __init__(self, board: Board, red_pin: Union[str, int], green_pin: Union[str, int], blue_pin: Union[str, int]):

        # create the 3 leds for each color
        self.__red_led = Led(board, red_pin)
        self.__green_led = Led(board, green_pin)
        self.__blue_led = Led(board, blue_pin)

        # Initialises the led to off
        # TO ACCESS THE PRIVATE VARIABLE from the parent class
        # USE THE FOLLOWING SYNTAX: self.__data
        self.__data = False

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
        Turn the ledrgb on \n
        """
        self.__data = True  # Set the status of the ledrgb to on
        self.__red_led.on()  # Turn on the Red LED
        self.__green_led.on()  # Turn on the Green LED
        self.__blue_led.on()  # Turn on the Blue LED

    def off(self):
        """
        Turn the ledrgb off \n
        """
        self.__data = False  # Set the status of the ledrgb to off
        self.__red_led.off()  # Turn off the Red LED
        self.__green_led.off()  # Turn off the Green LED
        self.__blue_led.off()  # Turn off the Blue LED

    @property
    def red(self):
        """
        Get or Set the value of the red [0-255]\n
        """
        return self.__red_led.intensity

    @red.setter
    def red(self, intensity: int):
        self.__red_led.intensity = intensity

    @property
    def green(self):
        """
        Get or Set the value of the green [0-255]\n
        """
        return self.__green_led.intensity

    @green.setter
    def green(self, intensity: int):
        self.__green_led.intensity = intensity

    @property
    def blue(self):
        """
        Get or Set the value of the blue [0-255]\n
        """
        return self.__blue_led.intensity

    @blue.setter
    def blue(self, intensity: int):
        self.__blue_led.intensity = intensity

    @property
    def rgb(self):
        """
        Get or Set the value of the rgb [0-255, 0-255, 0-255]\n
        """
        return self.__red_led.intensity, self.__green_led.intensity, self.__blue_led.intensity

    @rgb.setter
    def rgb(self, rgb: tuple):
        self.__red_led.intensity = rgb[0]
        self.__green_led.intensity = rgb[1]
        self.__blue_led.intensity = rgb[2]

    @property
    def data(self):
        """
        Get the status of the ledrgb (on or off)\n
        """
        return self.__data

    @data.setter
    def data(self, data: bool):
        if data:
            self.on()
        else:
            self.off()
