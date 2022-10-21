from alimata.core.core import is_async_function, PIN_MODE
from alimata.sensors.sensor import Sensor
from alimata.core.board import Board


class Button(Sensor):
    """
    A class used to represent a Button

    Attributes
    ----------
    pin : str
        the pin of the Button
    invert : bool
        if the button is inverted or not

    Properties
    ----------
    data : bool
        the value of the Button (Pressed (True) or Released (False))
    """


    # Instead of using self.__data, we use self._Sensor__data

    def __init__(self, board: Board, pin: str, invert: bool = False, callback=None):
        
        Sensor.__init__(self, board=board, pin=pin, type=PIN_MODE.PULLUP)

        # Initialises the button as not pressed
        self.__data = False # PRIVATE

        # Initialises the Callback function that is *user defined*
        self.__callback = callback # PRIVATE

        # Initialises the invert value
        self.invert = invert # PUBLIC


    # ABSTRACT FROM SENSOR
    @property
    def data(self):
        """Return the current status of the button (True or False)"""
        return self.__data


    # ABSTRACT FROM SENSOR
    # Change the status of the button when pressed
    # Back end callback function (*not user defined*)
    async def is_changed_callback(self, data):
        try:
            if Sensor.is_ready(self):

                # Check if the button is inverted
                self.__data = not bool(data[2]) if self.invert else bool(data[2])

                # Check if the user has defined a callback function
                if self.__callback is not None:

                    # Check if the callback function is async
                    if is_async_function(self.__callback):
                        await self.__callback(self)
                    else:
                        self.__callback(self)
                        
        except Exception as e:
            print(e)
