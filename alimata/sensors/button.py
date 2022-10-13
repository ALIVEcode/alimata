from alimata.core.core import is_async_function, PIN_MODE
from alimata.sensors.sensor import Sensor
from alimata.core.board import Board
import asyncio


class Button(Sensor):

    # Return the current status of the button
    def is_pressed(self):
        return self.__value

    # Change the status of the button when pressed
    async def _is_pressed_callback(self, data):
        if self.invert:
            self.__value = not bool(data[2])
        else:
            self.__value = bool(data[2])

        if self.__callback is not None:
            if is_async_function(self.__callback):
                await self.__callback(data)
            else:
                self.__callback(data)

    # Set the pin and callback of the button
    # call this method if you initialize the class in an async function
    async def async_init(self):
        await self.board.set_pin_mode(self.pin, PIN_MODE.PULLUP, self._is_pressed_callback)

    def __init__(self, board: Board, pin, invert: bool = False, callback=None):
        self.board = board
        self.pin = pin
        self.invert = invert
        self.__value = None
        self.__callback = callback

        self.callback = callback or self._is_pressed_callback

        # set the event loop
        self.loop = asyncio.get_event_loop()

        # Start the async init
        self.loop.run_until_complete(self.async_init())
