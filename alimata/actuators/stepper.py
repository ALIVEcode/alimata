from alimata.actuators.actuator import Actuator
from alimata.core.board import Board
from alimata.core.core import PIN_MODE, STEPPER_TYPE, print_warning
from typing import Union, Optional


class Stepper(Actuator):

    def __init__(self, board: Board, stepper_type: STEPPER_TYPE, pin1: Union[str, int], pin2: Union[str, int],
                 pin3: Optional[Union[str, int]] = None, pin4: Optional[Union[str, int]] = None, max_speed: int = 1000):

        if pin3 is None and pin4 is None:
            pin_ = [pin1, pin2, None, None]
        elif pin3 is not None and pin4 is None:
            pin_ = [pin1, pin2, pin3 , None]
        elif pin3 is not None and pin4 is not None:
            pin_ = [pin1, pin2, pin3, pin4]
        else:
            raise ValueError("You must provide 2, 3 or 4 pins")

        super().__init__(pin=pin_, board=board, type_=PIN_MODE.STEPPER, stepper_type=stepper_type)

        self.current_position = 0

        self.__max_speed = max_speed
        self.__set_max_speed(max_speed=max_speed)

        self.__speed = 200
        self.speed = self.__speed

        self.__enable = True

        self.__min_pulse_width = -1

        self.__acceleration = 800
        self.acceleration = self.__acceleration

        self.__callback_value = [0]

        print("Stepper initialized | ID : " + str(self.id))

    @property
    def motor_id(self) -> int:
        '''Returns the motor id'''
        return self.id

    @property
    def current_position(self, callback=None) -> int:
        '''Returns the current position of the stepper motor'''
        self.board.firmetix_board.stepper_get_current_position(self.motor_id,
                                                               lambda data: self.__callback(data,
                                                                                            user_callback=callback))
        return self.__wait_for_callback(17)[2]
    
    @current_position.setter
    def current_position(self, position:int):
        '''Resets the current position of the motor'''
        self.board.firmetix_board.stepper_set_current_position(self.motor_id, position)

    @property
    def target_position(self, callback=None) -> int:
        '''Returns the target position of the stepper motor'''
        self.board.firmetix_board.stepper_get_target_position(self.motor_id,
                                                              lambda data: self.__callback(data,
                                                                                           user_callback=callback))
        return self.__wait_for_callback(16)[2]

    @property
    def distance_to_go(self, callback=None) -> int:
        '''Returns the distance to go'''
        self.board.firmetix_board.stepper_get_distance_to_go(self.motor_id,
                                                             lambda data: self.__callback(data, user_callback=callback))
        return self.__wait_for_callback(15)[2]

    @property
    def max_speed(self) -> int:
        '''Returns the max speed'''
        return self.__max_speed

    @property
    def speed(self) -> int:
        '''Set or get the speed of the stepper motor'''
        return self.__speed

    @speed.setter
    def speed(self, speed: int):
        self.board.firmetix_board.stepper_set_speed(self.motor_id, speed)
        self.__speed = speed

    @property
    def acceleration(self) -> int:
        '''Set or get the acceleration in steps per second'''
        return self.__acceleration
    
    @acceleration.setter
    def acceleration(self, acceleration: int):
        self.board.firmetix_board.stepper_set_acceleration(self.motor_id, acceleration)
        self.__acceleration = acceleration

    @property
    def enable(self) -> bool:
        '''Enable or disable the stepper motor output'''
        return self.__enable

    @enable.setter
    def enable(self, enable: bool):
        if enable:
            self.board.firmetix_board.stepper_enable_outputs(self.motor_id)
        else:
            self.board.firmetix_board.stepper_disable_outputs(self.motor_id)
        self.__enable = enable

    @property
    def min_pulse_width(self) -> int:
        '''Get or set the minimum pulse width in microseconds'''
        return self.__min_pulse_width

    @min_pulse_width.setter
    def min_pulse_width(self, min_pulse_width: int):
        self.board.firmetix_board.stepper_set_min_pulse_width(self.motor_id, min_pulse_width)
        self.__min_pulse_width = min_pulse_width

    def running(self, callback=None) -> bool:
        '''Returns True if the stepper motor is running'''
        self.board.firmetix_board.stepper_is_running(self.motor_id,
                                                     lambda data: self.__callback(data, user_callback=callback))
        return self.__wait_for_callback(18)[2]

    def new_home(self):
        '''Sets the current position as the new home'''
        self.board.firmetix_board.stepper_set_current_position(self.motor_id, self.current_position)
        self.speed = self.__speed  # Reset the speed back to his original value

    def home(self, callback=None) -> bool:
        '''Moves the stepper motor to the home position \n retrun True when done'''
        return self.move_to(0, callback=callback)

    def move(self, relative_position: int, callback=None, blocking: bool = True) -> bool:
        '''Moves the stepper motor to the relative position \n retrun True when done or if we're not blocking'''
        if not self.__is_enabled():
            print_warning("The stepper motor is not enabled skipping instruction")
            return False
        self.board.firmetix_board.stepper_move(self.motor_id, relative_position)
        self.board.firmetix_board.stepper_run_speed_to_position(self.motor_id,
                                                                lambda data: self.__callback(data,
                                                                                             user_callback=callback))
        if blocking:
            return self.__wait_for_callback(19)
        return True

    def move_to(self, absolute_position: int, callback=None, blocking: bool = True) -> bool:
        '''Moves the stepper motor to an absolute position \n retrun True when done or if we're not blocking'''
        if not self.__is_enabled():
            print_warning("The stepper motor is not enabled skipping instruction")
            return False
        self.board.firmetix_board.stepper_move_to(self.motor_id, absolute_position)
        self.board.firmetix_board.stepper_run_speed_to_position(self.motor_id,
                                                                lambda data: self.__callback(data,
                                                                                             user_callback=callback))
        if blocking:
            return self.__wait_for_callback(19)
        return True

    def run(self):
        '''Run the stepper motor at the current speed until stopped'''
        self.board.firmetix_board.stepper_run(self.motor_id, lambda data: self.__callback(data, user_callback=None))

    def stop(self):
        '''Stops the stepper motor'''
        self.board.firmetix_board.stepper_stop(self.motor_id)

    # Should only be called in the init function
    def __set_max_speed(self, max_speed: int):
        '''Sets the max speed of the stepper motor'''
        self.board.firmetix_board.stepper_set_max_speed(self.motor_id, max_speed)
        self.__max_speed = max_speed

    def __is_enabled(self) -> bool:
        '''Returns True if the stepper motor is enabled'''
        return self.__enable

    def __callback(self, data, user_callback=None):
        if user_callback is not None:
            user_callback(data)
        self.__callback_value = data

    def __wait_for_callback(self, report_id: int) -> Union[list, bool]:
        '''
            Waits for the callback to be called and returns the value if the report id is the same \n 
            15 = distance_to_go, \n
            16 = target_position, \n
            17 = current_position, \n
            18 = stepper_is_running \n
            19 = stepper_run (return a bool) \n
        '''
        # list [report_id, motor_id, value, time_stamp]
        while self.__callback_value[0] != report_id:
            # TODO: possibly add a timeout
            pass

        if self.__callback_value[0] == 19:
            return True

        return self.__callback_value
