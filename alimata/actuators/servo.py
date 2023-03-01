from alimata.actuators.actuator import Actuator
from alimata.core.board import Board
from alimata.core.core import PIN_MODE, WRITE_MODE, map_range, print_warning, normalize_angle
import time
from typing import Union
from threading import Thread


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
    move_to(end_angle: int, duration: int = 0, threaded: bool = False)
        Move the servo to the given angle in the given time in ms (optional)
        Run it in parallel if threaded is True (optional)
    stop()
        Stop the servo
    """

    def __init__(self, board: Board, pin_: Union[str, int], min_pulse: int = 544, max_pulse: int = 2400):
        super().__init__(pin=pin_, board=board, type_=PIN_MODE.SERVO, min_pulse=min_pulse, max_pulse=max_pulse)

        # Initialises the servo to not moving
        self.__running = False

        # Initialises the servo to 0 degrees
        self.__data = 0
        self.data = 0

        self.__thread = None

    @property
    def data(self):
        """Return the current angle of the servo"""
        return self.__data

    @data.setter
    def data(self, angle: int):
        """Set the angle of the servo"""
        if self.__running:
            print_warning("Servo currently running, stop the servo before setting the angle")
            return

        self.__data = normalize_angle(angle)
        self.board.write_to_pin(pin=self.pin, type_=WRITE_MODE.SERVO, value=self.__data)

    @property
    def running(self):
        """Return True if the servo is runing"""
        return self.__running

    def stop(self):
        """Stop the servo"""
        self.__running = False
        self.__thread = None

    def move_to(self, end_angle: int, duration: int = 0, wait: bool = True):
        """
        Move the servo to the given angle in the given time in ms (optional),
        do it in parallel if threaded is True (optional)
        """
        if self.__running:
            print_warning("Servo currently running, stop the servo before setting the angle")
            return

        if duration == 0:
            self.data = end_angle
            return

        if not wait:
            self.__thread = Thread(target=self.__move, args=(end_angle, duration))
            self.__thread.start()
        else:
            self.__move(end_angle, duration)

    def __move(self, end_angle: int, duration: int = 0):
        self.__running = True
        start_angle = self.__data
        start_time = time.time()
        normalized_end_angle = normalize_angle(end_angle)
        i = None

        while self.__running:
            elapsed_time = (time.time() - start_time) * 1000
            if elapsed_time > duration or i == normalized_end_angle:
                self.board.write_to_pin(self.pin, WRITE_MODE.SERVO, normalized_end_angle)
                self.__running = False
                self.__thread = None
                break
            else:
                i = int(map_range(elapsed_time, 0, duration, start_angle, normalized_end_angle))
                self.board.write_to_pin(self.pin, WRITE_MODE.SERVO, i)
                time.sleep(0.01)
