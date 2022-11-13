from alimata.core.core import DHT_TYPE, PIN_MODE, WRITE_MODE, I2C_COMMAND, print_warning
from alimata.core.error import AlimataUnexpectedPin
from pymata4 import pymata4
from typing import Optional, Union
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
    pymata_board : telemetrix
        The telemetrix board object (read only)
    set_pin_mode : function
        Setting the pin mode : (pin, type, callback=None, differential=1, echo_pin=None, min_pulse=544, max_pulse=2400)
    write_pin : function
        Writing to a pin : (pin, type, value, duration, step)
    i2C_comunication : function
        Sending a i2c command : (command, adress, register, number_of_bytes, args, callback)
    parse_pin_number : function
        Converting the analog pin value to the correct one depending on the board and function used : (pin, pin_type)
    
    """

    def __init__(self, board_id: int = 1, COM_port=None):
        self.__board = pymata4.Pymata4(arduino_instance_id=board_id, com_port=COM_port, arduino_wait=2)
        self.__board_id = board_id
        self.__is_started = False

        self.__setup_func = None
        self.__loop_func = None

        self.__num_of_digital_pins = len(self.__board.digital_pins)

    
    def __main(self):
        # start the setup function
        self.__setup_func()

        # loop the loop function
        while self.__is_started:
            self.__loop_func()

    def start(self, setup_func = None, loop_func = None):
        if self.__is_started == True:
            print_warning("Board is already started, not starting again")
            return
        elif setup_func is not None and loop_func is not None:
            
            # saving the functions
            self.__setup_func = setup_func
            self.__loop_func = loop_func


            try:
                    
                self.__is_started = True
                print("Board started")
                
                # start the main function
                self.__main()

            except (KeyboardInterrupt, RuntimeError) as e:
                self.shutdown()
                sys.exit(0)
        elif setup_func is None or loop_func is None:
            raise TypeError("Both setup_func and loop_func must be defined or none of them")
        else:
            self.__is_started = True
            print("Board started")

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
    def parse_pin_number(self, pin: Union[str, int, list], type_) -> int:
        if type(pin) == str:
            if pin.startswith("A"): #Check if it's an analog pin
                pin = int(pin[1:]) #Strip the A from the pin name
                if type_ != PIN_MODE.ANALOG_INPUT:
                    pin = int(pin) + self.__num_of_digital_pins
        elif type(pin) == list:
            mapped_pin = pin.copy()
            for i in range(len(pin)):
                mapped_pin[i] = self.parse_pin_number(pin[i], type_)
            return mapped_pin
            
        if type(pin) is not int:
            raise AlimataUnexpectedPin("The pin must either be in an int (1, 2, 3 ...) or a string (A1, A2, A3 ...)")
        return int(pin)


    def set_pin_mode(self, pin: Union[str, int, list], type_: PIN_MODE, callback=None, dht_type: Optional[DHT_TYPE] = None, timeout=80000, differential: int = 1, min_pulse: int = 544, max_pulse:int =2400, steps_per_revolution: Optional[int] = None):
        parsed_pin = self.parse_pin_number(pin=pin, type_=type_)
        
        if type_ == PIN_MODE.DIGITAL_INPUT:
            self.__board.set_pin_mode_digital_input(pin_number=parsed_pin, callback=callback)
        elif type_ == PIN_MODE.DIGITAL_OUTPUT:
            self.__board.set_pin_mode_digital_output(pin_number=parsed_pin)
        elif type_ == PIN_MODE.PULLUP:
            self.__board.set_pin_mode_digital_input_pullup(pin_number=parsed_pin, callback=callback)
        elif type_ == PIN_MODE.ANALOG_INPUT:
            self.__board.set_pin_mode_analog_input(pin_number=parsed_pin, differential=differential, callback=callback)
        elif type_ == PIN_MODE.ANALOG_OUTPUT:
            self.__board.set_pin_mode_pwm_output(pin_number=parsed_pin)
        elif type_ == PIN_MODE.SONAR:
            if type(parsed_pin) is not list:
                raise TypeError("pin must be a list (trigger_pin, echo_pin)")
            else:
                self.__board.set_pin_mode_sonar(trigger_pin=parsed_pin[0], echo_pin=parsed_pin[1], callback=callback, timeout=timeout)
        elif type_ == PIN_MODE.DHT:
            if dht_type is None:
                raise TypeError("dht_type is required to setup a dht")
            self.__board.set_pin_mode_dht(pin_number=parsed_pin, callback=callback, sensor_type=dht_type, differential=differential)
        elif type_ == PIN_MODE.SERVO:
            self.__board.set_pin_mode_servo(oin=parsed_pin, min_pulse=min_pulse, max_pulse=max_pulse)
        elif type_ == PIN_MODE.STEPPER:
            if type(parsed_pin) is not list:
                raise TypeError("pin must be a list of 2 or 4 pins")
            elif steps_per_revolution is None:
                raise TypeError("steps_per_revolution is required to setup a stepper")
            else:
                self.__board.set_pin_mode_stepper(steps_per_revolution=steps_per_revolution, stepper_pins=parsed_pin)
        elif type_ == PIN_MODE.TONE:
            self.__board.set_pin_mode_tone(pin_number=parsed_pin)
        elif type_ == PIN_MODE.I2C:
            self.__board.set_pin_mode_i2c(read_delay_time=parsed_pin) #I2C doesn't need a pin number so we use the pin parameter as the read_delay_time
        else:
            raise TypeError("type must a value from the PIN_MODE enum")

        
    # Use PWM for analog write
    def write_to_pin(self, pin: Union[str, int], type_: WRITE_MODE, value: int, duration: Optional[int] = None, number_of_steps: Optional[int] = None):
        parsed_pin = self.parse_pin_number(pin=pin, type_=type_)

        # Analog OUTPUT
        if type_ == WRITE_MODE.ANALOG:
            if value >= 0 or value <= 255:
                self.__board.pwm_write(pin=parsed_pin, value=value)
            elif value > 255:
                print_warning("Value is greater than 255, setting value to 255")
                self.__board.pwm_write(pin=parsed_pin, value=255)
            elif value < 0:
                print_warning("Value is less than 0, setting value to 0")
                self.__board.pwm_write(pin=parsed_pin, value=0)

        # Digital OUTPUT
        elif type_ == WRITE_MODE.DIGITAL:
            if value not in [0, 1]:
                raise TypeError("value must be equal to 0 or 1")
            else:
                self.__board.digital_write(pin=parsed_pin, value=value)
        elif type_ == WRITE_MODE.SERVO:
            self.__board.servo_write(pin=parsed_pin, value=value)
        elif type_ == WRITE_MODE.STEPPER:
            if number_of_steps is None:
                raise TypeError("number_of_steps is required to write to a stepper")
            else:
                self.__board.stepper_write(motor_speed=value, number_of_steps=number_of_steps)

        # Tone Duration OUTPUT
        elif type_ == WRITE_MODE.TONE:
            if duration is None:
                raise TypeError("duration (in ms) is required for tone")
            self.__board.play_tone(pin_number=parsed_pin, frequency=value, duration=duration)
        elif type_ == WRITE_MODE.TONE_CONTINUOUS:
            self.__board.play_tone_continuously(pin_number=parsed_pin, frequency=value)
        elif type_ == WRITE_MODE.TONE_STOP:
            self.__board.play_tone_off(pin_number=parsed_pin)
        else:
            raise TypeError("type must be one of the WRITE_MODE enum")
    
    def i2c_comunication(self, command: I2C_COMMAND, adress, register = None, number_of_bytes = None, args: list = None, callback = None):
        if command == I2C_COMMAND.READ:
            if number_of_bytes is None or register is None:
                raise TypeError("number_of_bytes and register are required to read from i2c")
            else:
                self.__board.i2c_read(address=adress, register=register, number_of_bytes=number_of_bytes, callback=callback)
        elif command == I2C_COMMAND.WRITE:
            if args is None :
                raise TypeError("args are required to write to i2c")
            else:
                self.__board.i2c_write(address=adress, args=args)
        elif command == I2C_COMMAND.READ_CONTINUOUS:
            if number_of_bytes is None or register is None:
                raise TypeError("number_of_bytes and register are required to read from i2c")
            else:
                self.__board.i2c_read_continuous(address=adress, register=register, number_of_bytes=number_of_bytes, callback=callback)
        elif command == I2C_COMMAND.READ_RESTART_TRANSMISSION:
            if number_of_bytes is None or register is None:
                raise TypeError("number_of_bytes and register are required to read from i2c")
            else:
                self.__board.i2c_read_restart_transmission(address=adress, register=register, number_of_bytes=number_of_bytes, callback=callback)
        elif command == I2C_COMMAND.READ_SAVED_DATA:
            self.__board.i2c_read_saved_data(adress=adress)
        else:
            raise TypeError("command must be one of the I2C_COMMAND enum")
    
    @property
    def pymata_board(self):
        return self.__board