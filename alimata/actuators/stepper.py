from alimata.actuators.actuator import Actuator
from alimata.core.board import Board
from alimata.core.core import PIN_MODE, WRITE_MODE, print_warning
from typing import Union, Optional

class Stepper(Actuator):
    
    def __init__(self, board: Board, steps_per_revolution: int, pin1: Union[str, int], pin2: Union[str, int], pin3: Optional[Union[str, int]] = None, pin4:  Optional[Union[str, int]] = None, speed: int = 5):
        raise NotImplementedError("Stepper not implemented yet")

        
        if pin3 is None and pin4 is None:
            pin_ = [pin1, pin2]
        elif pin3 is not None and pin4 is not None:
            pin_ = [pin1, pin2, pin3, pin4]
        else:
            raise ValueError("You must provide 2 or 4 pins")

        super().__init__(pin=pin_, board=board, type_=PIN_MODE.STEPPER, steps_per_revolution=steps_per_revolution)
        
        #Set the speed of the stepper
        self.__speed = speed

    @property
    def speed(self):
        """Return the speed of the stepper"""
        return self.__speed
    
    @speed.setter
    def speed(self, speed: int):
        """Set the speed of the stepper (rotation per minute)"""
        self.__speed = abs(speed)
    
    def step(self, steps: int, speed: Optional[int] = None):
        """Move the stepper of the given number of steps (negative for reverse)"""
        if speed is not None:
            self.__speed = abs(speed)
            
        self.board.write_to_pin(pin=self.pin, type_=WRITE_MODE.STEPPER, value=self.__speed, number_of_steps=steps)

    def stop(self):
        """NOT WORKING : Stop the stepper"""
        self.board.write_to_pin(pin=self.pin, type_=WRITE_MODE.STEPPER, value=1, number_of_steps=0)
        
    