import imp
from alimata.core.core import PIN_MODE, WRITE_MODE, print_warning
from alimata.core.error import AlimataUnexpectedPin
from telemetrix import telemetrix
from typing import Union
import sys, datetime


class Board:
    """
    A class used to represent the arduino board

    Attributes
    ----------
    board_id : int
        The id of the board same as in telemetrix4arduino (read only)

    
    Methods
    ---------
    start(setup_func, loop_func)
        Starting the board : (setup_func, loop_func)
    is_started : bool
        Retuns if the board is started or not (read only)
    telemetrix_board : telemetrix
        The telemetrix board object (read only)
    set_pin_mode : function
        Setting the pin mode : (pin, type, callback=None, differential=1, echo_pin=None, min_pulse=544, max_pulse=2400)
    write_pin : function
        Writing to a pin : (pin, type, value, duration, step)
    parse_pin_number : function
        Converting the analog pin value to the correct one depending on the board and function used : (pin, pin_type)
    
    """

    def __init__(self, board_id: int = 1, COM_port=None):
        self.__board = telemetrix.Telemetrix(arduino_instance_id=board_id, com_port=COM_port, arduino_wait=2)
        self.__board_id = board_id
        self.__is_started = False

        self.__setup_func = None
        self.__loop_func = None

    def __main(self):
        # start the setup function
        self.__setup_func()

        
        self.__is_started = True

        # loop the loop function
        while self.__is_started:
            self.__loop_func()

    def start(self, setup_func, loop_func):
        if self.__is_started == True:
            print_warning("Board is already started, not starting again")
        else:

            # saving the functions
            self.__setup_func = setup_func
            self.__loop_func = loop_func


            try:
                # start the main function
                self.__main()

            except (KeyboardInterrupt, RuntimeError) as e:
                self.shutdown()
                sys.exit(0)

    def is_started(self):
        return self.__is_started
    
    @property
    def board_id(self):
        return self.__board_id

    def shutdown(self):
        self.__is_started = False

        print("\nSHUTING DOWN BOARD ! | ID : " + str(self.__board_id) + " | TIME : " + str(datetime.datetime.now().strftime("%H:%M:%S")))
        self.__board.shutdown()

    
    # Converting the analog pin value to the correct one depending on the board and function used
    def parse_pin_number(self, pin: Union[str, int], type_) -> int:
        if type(pin) == str:
            if pin.startswith("A"): #Check if it's an analog pin
                if type_ != PIN_MODE.ANALOG_INPUT or type_ != PIN_MODE.ANALOG_OUTPUT or type_ != WRITE_MODE.ANALOG:
                    raise AlimataUnexpectedPin("Can't assign a analog pin to a digital function")
                pin = pin[1:]
        return int(pin)


    def set_pin_mode(self, pin: Union[str, int], type_: PIN_MODE, callback=None, differential: int = 1, echo_pin: Union[str, int] = None, min_pulse: int = 544, max_pulse:int =2400):
        pin = self.parse_pin_number(pin, type_)
        
        if type_ == PIN_MODE.DIGITAL_INPUT:
            self.__board.set_pin_mode_digital_input(pin, callback)
        elif type_ == PIN_MODE.DIGITAL_OUTPUT:
            self.__board.set_pin_mode_digital_output(pin)
        elif type_ == PIN_MODE.PULLUP:
            self.__board.set_pin_mode_digital_input_pullup(pin, callback)
        elif type_ == PIN_MODE.ANALOG_INPUT:
            self.__board.set_pin_mode_analog_input(pin, differential, callback)
        elif type_ == PIN_MODE.ANALOG_OUTPUT:
            self.__board.set_pin_mode_analog_output(pin)
        elif type_ == PIN_MODE.SONAR:
            if echo_pin is None:
                raise TypeError("echo_pin is required to setup a sonar")
            else:
                self.__board.set_pin_mode_sonar(pin, echo_pin, callback)
        elif type_ == PIN_MODE.DHT:
            self.__board.set_pin_mode_dht(pin, callback)
        elif type_ == PIN_MODE.SERVO:
            self.__board.set_pin_mode_servo(pin, min_pulse, max_pulse)
        elif type_ == PIN_MODE.SERVO_DETATCH:
            self.__board.set_pin_mode_servo_detach(pin)
        else:
            raise TypeError("type must a value from the PIN_MODE enum")

        
    # Use PWM for analog write
    def write_to_pin(self, pin: Union[str, int], type_: WRITE_MODE, value: int):
        pin = self.parse_pin_number(pin, type_)

        if type == WRITE_MODE.ANALOG:
            if value >= 0 or value <= 255:
                self.__board.analog_write(pin, value)
            elif value > 255:
                print_warning("Value is greater than 255, setting value to 255")
                self.__board.analog_write(pin, 255)
            elif value < 0:
                print_warning("Value is less than 0, setting value to 0")
                self.__board.analog_write(pin, 0)
        elif type == WRITE_MODE.DIGITAL:
            if value not in [0, 1]:
                raise TypeError("value must be equal to 0 or 1")
            else:
                self.__board.digital_write(pin, value)
        elif type == WRITE_MODE.SERVO:
            self.__board.servo_write(pin, value)
        else:
            raise TypeError("type must be one of the WRITE_MODE enum")
    
    @property
    def telemetrix_board(self):
        return self.__board