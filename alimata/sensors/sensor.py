from alimata.core.board import Board
from typing import Callable, Optional

import asyncio
from abc import ABC, abstractmethod, abstractproperty

from alimata.core.core import is_async_function


class Sensor(ABC):
    """    
    Methods
    ----------------
    is_ready()
        Return True if the sensor is ready to be used

    Abstract Methods
    ----------------
    is_changed_callback(self, data)
        Callback when the sensor value has changed
    
    Abstract Properties
    ----------------
    data
        Return the current value of the sensor
    """

    # Constructor of the class Sensor
    def __init__(self, 
                pin: str, 
                board: Board,
                type_: str, 
                differential: int = 1, # Facultative
                echo_pin: str = None, # Facultative
                timeout: int = 8000, # Facultative
                sensor_type: int = 11, # Facultative
                on_change: Optional[Callable[[list], None]] = None
                ):

        # Create Public Attributes
        self.board = board
        self.pin = pin

        # Create Private Attributes
        self.__type = type_
        self.__differential = differential
        self.__echo_pin = echo_pin
        self.__timeout = timeout
        self.__sensor_type = sensor_type
        self.__on_change: Optional[Callable[[list], None]] = on_change


        # set the event loop
        self.loop = asyncio.get_event_loop()

        # Start the async init
        self.loop.run_until_complete(self.async_init())


    # Set the pin and callback of the sensor
    # call this method if you initialize the class in an async function
    async def async_init(self):
        await self.board.set_pin_mode(
            pin=self.pin,
            type_=self.__type,
            callback=self.__callback,
            differential=self.__differential,
            echo_pin=self.__echo_pin,
            timeout=self.__timeout,
            sensor_type=self.__sensor_type)
    
    def on_change(self, on_change: Callable[[list], None]):
        """Set the callback when the sensor value has changed"""
        self.__on_change = on_change

    async def __callback(self, data: list):
        try:
            await self._update_data(data)

            if not self.is_ready() or self.__on_change is None:
                return

            if is_async_function(self.__on_change):
                await self.__on_change(self)
            else:
                self.__on_change(self)
        except Exception as e:
            print(e)

    @abstractmethod
    async def _update_data(self, data):
        """Callback when the sensor's value has changed enough"""
        pass


    def is_ready(self) -> bool:
        """Return True if the sensor is ready to read (True or False)"""
        if self.data is None:  # self.data is a property of the child class
            return False
        return self.board.is_started()
        
    
    @property
    @abstractmethod
    def data(self):
        """Return the data of the sensor"""
        pass