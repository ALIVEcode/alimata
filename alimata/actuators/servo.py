from alimata.actuators.actuator import Actuator
from alimata.core.board import Board
from alimata.core.core import PIN_MODE, WRITE_MODE, maprange, print_warning, normalize_angle
import time

class Servo(Actuator):
    """
    A class used to represent a Servo
    
    Properties
    ----------
    data : int
        the angle of the servo (0-180)
    runing : bool
        the status of the servo (moving or not)
    
    Methods
    -------
    move_to(end_angle: int, duration: int = 0)
        Move the servo to the given angle in the given time in ms (optional)
    stop()
        Stop the servo
    detatch()
        Detatch the servo for reuse
    """

    def __init__(self, board: Board,  pin_: str, min_pulse: int = 544, max_pulse: int = 2400):
        super().__init__(pin=pin_, board=board, type_=PIN_MODE.SERVO, min_pulse=min_pulse, max_pulse=max_pulse)
        
        # Initialises the servo to not moving
        self.__runing = False

        # Initialises the servo to 0 degrees
        self.__data = 0
        self.data = 0

    
    @property
    def data(self):
        """Return the current angle of the servo"""
        return self.__data
    
    @data.setter
    def data(self, angle: int):
        """Set the angle of the servo"""
        if self.__runing:
            print_warning("Stoping servo, then setting angle")
            self.stop()
        
        self.__data = normalize_angle(angle)
        self.board.write_to_pin(pin=self.pin, type_=WRITE_MODE.SERVO, value=self.__data)
    
    @property
    def runing(self):
        """Return True if the servo is runing"""
        return self.__runing
    
    def stop(self):
        """Stop the servo"""
        self.__runing = False

    def detatch(self):
        """Detatch the servo"""
        self.board.set_pin_mode(self.pin, PIN_MODE.SERVO_DETATCH)
        
    
    def move_to(self, end_angle: int, duration: int = 0):
        """Move the servo to the given angle in the given time in ms (optional)"""
        if self.__runing:
            print_warning("Stoping servo, then setting angle")
            self.stop()

        if duration == 0:
            self.data = end_angle
            return

        self.__runing = True
        start_angle = self.__data
        start_time = time.time()
        normalized_end_angle = normalize_angle(end_angle)
        i = None

        while self.__runing:
            elapsed_time = (time.time() - start_time)*1000
            if elapsed_time > duration or i == normalized_end_angle:
                self.board.write_to_pin(self.pin, WRITE_MODE.SERVO, normalized_end_angle)
                self.__runing = False
                break
            else:
                i = int(maprange(elapsed_time, 0, duration, start_angle, normalized_end_angle))
                self.board.write_to_pin(self.pin, WRITE_MODE.SERVO, i)
                time.sleep(0.01)   