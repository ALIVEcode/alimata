from alimata.core.board import Board
from typing import Callable, Optional

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
                type_: str, 
                differential: int = 1, # Facultative
                echo_pin: str = None, # Facultative
                on_change: Optional[Callable[[list], None]] = None
                ):

        # Create Public Attributes
        self.board = board
        self.pin = pin

        # Create Private Attributes
        self.__type = type_
        self.__differential = differential
        self.__echo_pin = echo_pin
        self.__on_change: Optional[Callable[[list], None]] = on_change

        # Set the pin and callback of the sensor
        self.board.set_pin_mode(
            pin=self.pin,
            type_=self.__type,
            callback=self.__callback,
            differential=self.__differential,
            echo_pin=self.__echo_pin)

    
    def on_change(self, on_change: Callable[[list], None]):
        """Set the callback when the sensor value has changed"""
        self.__on_change = on_change

    def __callback(self, data: list):
        try:
            self._update_data(data)

            if not self.is_ready() or self.__on_change is None:
                return

            #call the callback set in the init with the child as the argument
            self.__on_change(self)
        except Exception as e:
            print(e)

    @abstractmethod
    def _update_data(self, data):
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