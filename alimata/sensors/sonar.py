from alimata.core.core import is_async_function, PIN_MODE
from alimata.core.board import Board
from alimata.sensors.sensor import Sensor
import asyncio


class Sonar(Sensor):

    # Return the current distance of the sonar in cm
    def get_distance(self):
        return self.__value

    # Is called when the sensor changes value
    async def _value_changed_callback(self, data):
        self.__value = data[2]

        if self.__callback is not None:
            if is_async_function(self.__callback):
                await self.__callback(data)
            else:
                self.__callback(data)

    # Set the pins and callback of the sonar sensor
    # call this method if you initialize the class in an async function
    async def async_init(self):
        await self.board.set_pin_mode(self.trigger_pin, PIN_MODE.SONAR, self._value_changed_callback,
                                      echo_pin=self.echo_pin, timeout=self.timeout)

    def __init__(self, board: Board.board, trigger_pin, echo_pin, callback=None, timeout=8000):
        self.board = board
        self.trigger_pin = trigger_pin
        self.echo_pin = echo_pin
        self.__value = None
        self.__callback = callback
        self.timeout = timeout

        self.callback = callback or self._value_changed_callback

        # set the event loop
        self.loop = asyncio.get_event_loop()

        # Start the async init
        self.loop.run_until_complete(self.async_init())
