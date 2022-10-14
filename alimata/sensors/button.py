from alimata.core.core import is_async_function, PIN_MODE
from alimata.sensors.sensor import Sensor
from alimata.core.board import Board
import asyncio


class Button(Sensor):
    """
    A class used to represent a Button

    Attributes
    ----------
    value : bool
        the value of the Button (Pressed or Released)
    pin : str
        the pin of the Button
    invert : bool
        if the button is inverted or not
    """

    def __init__(self, board: Board, pin: str, invert: bool = False, callback=None):
        self.board = board
        self.pin = pin
        self.invert = invert
        self.__value = False
        self.__callback = callback

        # self.callback = callback or self.__is_pressed_callback

        # set the event loop
        self.loop = asyncio.get_event_loop()

        # Start the async init
        self.loop.run_until_complete(self.async_init())



    # Set the pin and callback of the button
    # call this method if you initialize the class in an async function
    async def async_init(self):
        await self.board.set_pin_mode(self.pin, PIN_MODE.PULLUP, self.__has_changed_callback)


    @property
    def value(self):
        """Return the current status of the button (True or False)"""
        return self.__value


    # Change the status of the button when pressed
    async def __has_changed_callback(self, data):
        try:
            if self.invert:
                self.__value = not bool(data[2])
            else:
                self.__value = bool(data[2])

            if self.__callback is not None and self.board.is_started:
                if is_async_function(self.__callback):
                    await self.__callback(self)
                else:
                    self.__callback(self)
        except Exception as e:
            print(e)
