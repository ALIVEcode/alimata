from alimata.core.board import Board
from alimata.core.core import PIN_MODE, WRITE_MODE

import asyncio
from abc import ABC, abstractmethod

class Actuator(ABC):

   # Constructor of the class Actuator
    def __init__(self, 
    pin: str, 
    board: Board,
    type: str,
    min_pulse: int = 544,
    max_pulse: int = 2400,
    step_per_revolution: int = None
    ):

        # Create Public Attributes
        self.board = board
        self.pin = pin

        # Create Private Attributes
        self.__type = type
        self.__min_pulse = min_pulse
        self.__max_pulse = max_pulse
        self.__step_per_revolution = step_per_revolution


        self.__data = None

        # set the event loop
        self.loop = asyncio.get_event_loop()

        # Start the async init
        self.loop.run_until_complete(self.async_init())


    # Set the pin and other properties of the actuator
    # call this method if you initialize the class in an async function
    async def async_init(self):
        await self.board.set_pin_mode(
            pin=self.pin,
            type=self.__type,
            min_pulse=self.__min_pulse,
            max_pulse=self.__max_pulse,
            step_per_revolution=self.__step_per_revolution)

    @property
    def data(self):
        """Return the data of the actuator"""
        return self.__data	
    @data.setter
    def data(self, value):
        """Set the data of the actuator"""
        self.__data = value