from alimata.core.board import Board
from alimata.core.core import DHT_SENSOR_TYPE, PIN_MODE

import asyncio
from abc import ABC, abstractmethod, abstractproperty


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
    type: str, 
    differential: int = 1, # Facultative
    echo_pin: str = None, # Facultative
    timeout: int = 8000, # Facultative
    sensor_type: int = 11 # Facultative
    ):

        # Create Public Attributes
        self.board = board
        self.pin = pin

        # Create Private Attributes
        self.__type = type
        self.__differential = differential
        self.__echo_pin = echo_pin
        self.__timeout = timeout
        self.__sensor_type = sensor_type


        # set the event loop
        self.loop = asyncio.get_event_loop()

        # Start the async init
        self.loop.run_until_complete(self.async_init())


    # Set the pin and callback of the sensor
    # call this method if you initialize the class in an async function
    async def async_init(self):
        await self.board.set_pin_mode(
            pin=self.pin,
            type=self.__type,
            callback=self.is_changed_callback,
            differential=self.__differential,
            echo_pin=self.__echo_pin,
            timeout=self.__timeout,
            sensor_type=self.__sensor_type)
    
    @abstractmethod
    async def is_changed_callback(self, data):
        """Callback when the sensor's value has changed enough"""
        pass


    def is_ready(self) -> bool:
        """Return True if the sensor is ready to read (True or False)"""
        if self.data == None: # self.data is a property of the child class
            return False
        else:
            if self.board.is_started():
                return True
            else:
                return False
        
    
    @abstractproperty
    def data(self):
        """Return the data of the sensor"""
        pass