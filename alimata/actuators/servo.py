import asyncio
from alimata.actuators.actuator import Actuator
from alimata.core.board import Board
from alimata.core.core import PIN_MODE, WRITE_MODE, maprange, print_warning
import time

class Servo(Actuator):

    def __init__(self, board: Board,  pin_: str | int, min_pulse: int = 544, max_pulse: int = 2400):
        super().__init__(pin=pin_, board=board, type_=PIN_MODE.SERVO, min_pulse=min_pulse, max_pulse=max_pulse)
        self._Actuator__data = 0
        self.__runing = False
    
    @property
    def data(self):
        """Return the current angle of the servo"""
        return self._Actuator__data
    
    @data.setter
    def data(self, angle: int):
        """Set the angle of the servo"""
        if self.__runing:
            print_warning("Stoping servo, then setting angle")
            self.stop()
        self._Actuator__data = angle
        self.board.write_to_pin(self.pin, WRITE_MODE.SERVO, angle)
    
    @property
    def runing(self):
        """Return True if the servo is runing"""
        return self.__runing
    
    def stop(self):
        """Stop the servo"""
        self.__runing = False
        
    
    def move_to(self, end_angle: int, duration: int):
        """Move the servo to the given angle in the given time (in ms)"""
        if self.__runing:
            return
        else:
            self.__runing = True
            asyncio.create_task(self.__async_move_to(end_angle, duration))
    
    async def __async_move_to(self, end_angle:int, duration: int):
        start_angle = self.data
        start_time = time.time()
        while self.__runing:
            elapsed_time = (time.time() - start_time)*1000
            #print(elapsed_time)
            if elapsed_time > duration:
                self.board.write_to_pin(self.pin, WRITE_MODE.SERVO, end_angle)
                self.__runing = False
                break
            else:
                i = int(maprange(elapsed_time, 0, duration, start_angle, end_angle))
                self.board.write_to_pin(self.pin, WRITE_MODE.SERVO, i)
                await asyncio.sleep(0.01)   