from alimata.actuators.led import Led
from alimata.core.board import Board
from alimata.core.core import WRITE_MODE
from alimata.actuators.actuator import Actuator
import asyncio

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

    def __init__(self, board: Board, redPin, greenPin, bluePin):


        # create the 3 leds for each color
        self.__RedLed = Led(board, redPin)
        self.__GreenLed = Led(board, greenPin)
        self.__BlueLed = Led(board, bluePin)
        


        # Initialises the led to off
        # TO ACCESS THE PRIVATE VARIABLE from the parent class
        # USE THE FOLLOWING SYNTAX: self._Actuator__data
        self._Actuator__data = False


    
    def toggle(self):
        """
        Toggle the led on or off \n
        """
        if self._Actuator__data:
            self.off()
        else:
            self.on()

    def on(self):
        """
        Turn the ledrgb on \n
        """
        self._Actuator__data = True # Set the status of the ledrgb to on
        self.__RedLed.on() # Turn on the Red LED
        self.__GreenLed.on() # Turn on the Green LED
        self.__BlueLed.on() # Turn on the Blue LED


    def off(self):
        """
        Turn the ledrgb off \n
        """
        self._Actuator__data = False # Set the status of the ledrgb to off
        self.__RedLed.off() # Turn off the Red LED
        self.__GreenLed.off() # Turn off the Green LED
        self.__BlueLed.off() # Turn off the Blue LED

    @property
    def red(self):
        """
        Get or Set the value of the red [0-255]\n
        """
        return self.__RedLed.intensity

    @red.setter
    def red(self, intensity: int):
        self.__RedLed.intensity = intensity

    @property
    def green(self):
        """
        Get or Set the value of the green [0-255]\n
        """
        return self.__GreenLed.intensity
     
    @green.setter
    def green(self, intensity: int):    
        self.__GreenLed.intensity = intensity

    @property
    def blue(self):
        """
        Get or Set the value of the blue [0-255]\n
        """
        return self.__BlueLed.intensity

    @blue.setter
    def blue(self, intensity: int):
        self.__BlueLed.intensity = intensity

    @property
    def rgb(self):
        """
        Get or Set the value of the rgb [0-255, 0-255, 0-255]\n
        """
        return (self.__RedLed.intensity, self.__GreenLed.intensity, self.__BlueLed.intensity)

    @rgb.setter
    def rgb(self, rgb: tuple):
        self.__RedLed.intensity = rgb[0]
        self.__GreenLed.intensity = rgb[1]
        self.__BlueLed.intensity = rgb[2]
        
    @property
    def data(self):
        """
        Get the status of the ledrgb (on or off)\n
        """
        return self._Actuator__data
    
    @data.setter
    def data(self, data: bool):
        if data:
            self.on()
        else:
            self.off()
