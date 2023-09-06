import datetime
import sys
from typing import Optional, Union

from firmetix import firmetix
from firmetix.private_constants import Connection_type

from alimata.core.core import DHT_TYPE, PIN_MODE, WRITE_MODE, I2C_COMMAND, SPI_COMMAND, STEPPER_TYPE, CONNECTION_TYPE, print_warning
from alimata.core.error import AlimataUnexpectedPin, AlimataUnexpectedPinMode, AlimataUnexpectedWriteMode, \
    AlimataUnexpectedValue, AlimataUnexpectedI2cCommand, AlimataExpectedValue, AlimataCallbackNotDefined, \
    AlimataExpectedParameters


class Board:
    """
    A class used to represent the arduino board

    Attributes
    ----------
    board_id (optional) : int
        The id of the board same as in firmetix4arduino (read only)
    COM_port (optional)  : str
        The COM port of the board if it is connected with a serial connection (read only)
    connection_type (optional) : CONNECTION_TYPE
        The connection type of the board (read only) (CONNECTION_TYPE.SERIAL, CONNECTION_TYPE.WIFI, CONNECTION_TYPE.BLUETOOTH)
    ip_address (optional) : str
        The ip address of the board if it is connected with a wifi connection (read only)
    ble_mac_address (optional) : str
        The mac address of the board if it is connected with a bluetooth connection (read only)
    ble_name (optional) : str
        The name of the board if it is connected with a bluetooth connection (read only)

    
    Methods
    ---------
    start(setup_func, loop_func)
        Starting the board : (setup_func, loop_func)
    is_started : bool
        Retuns if the board is started or not (read only)
    firmetix_board : telemetrix
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

    def __init__(self, board_id: int = 1, COM_port=None, connection_type: CONNECTION_TYPE=CONNECTION_TYPE.SERIAL,  ip_address=None, ble_mac_address=None, ble_name=None):
        self.__board = firmetix.Firmetix(arduino_instance_id=board_id, com_port=COM_port, arduino_wait=2, connection_type=connection_type, ip_address=ip_address, ble_mac_address=ble_mac_address, ble_name=ble_name)
        self.__board_id = board_id
        self.__is_started = False

        self.__setup_func = None
        self.__loop_func = None

    def __main(self):
        # start the setup function
        if self.__setup_func is not None:
            self.__setup_func()

        # loop the loop function
        while self.__is_started:
            if self.__loop_func is not None:
                self.__loop_func()

    def start(self, setup_func=None, loop_func=None):
        """Start the board with the setup and loop fonctions or no functions"""
        if self.__is_started:
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

            except (KeyboardInterrupt, RuntimeError):
                self.shutdown()
                sys.exit(0)
        elif setup_func is None and setup_func is not None or loop_func is None and setup_func is not None:
            raise AlimataExpectedParameters("Both setup_func and loop_func must be defined or none of them")
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

        print("\nSHUTING DOWN BOARD ! | ID : " + str(self.__board_id) + " | TIME : " + str(
            datetime.datetime.now().strftime("%H:%M:%S")))
        self.__board.shutdown()

    # Converting the analog pin value to the correct one depending on the board and function used
    def parse_pin_number(self, pin: Union[str, int, list], type_) -> Union[int, list]:
        if type(pin) == str:
            if pin.startswith("A"):  # Check if it's an analog pin
                pin = int(pin[1:])  # Strip the A from the pin name
                if type_ != PIN_MODE.ANALOG_INPUT:
                    # If it's not an analog input, convert the pin to a digital pin
                    pin = pin + self.firmetix_board.first_analog_pin
            elif pin.isdigit():
                pin = int(pin)
            else:
                raise AlimataUnexpectedPin(
                    "The pin must either be in an int (1, 2, 3 ...) or a string (A1, A2, A3 ...)")
        elif type(pin) == list:
            mapped_pin = pin.copy()
            for i in range(len(pin)):
                mapped_pin[i] = self.parse_pin_number(pin[i], type_)
            return mapped_pin

        if type(pin) is not int:
            raise AlimataUnexpectedPin("The pin must either be in an int (1, 2, 3 ...) or a string (A1, A2, A3 ...)")
        return int(pin)

    def set_pin_mode(self, pin: Union[str, int, list], type_: PIN_MODE, callback=None,
                     dht_type: Optional[DHT_TYPE] = None, differential: int = 0, min_pulse: int = 544,
                     max_pulse: int = 2400, stepper_type: Optional[STEPPER_TYPE] = None):
        ''' Set the pin mode for the pins (return None execpt for stepper)'''
        parsed_pin = self.parse_pin_number(pin=pin, type_=type_)

        if type_ == PIN_MODE.DIGITAL_INPUT:
            if callback is None:
                raise AlimataCallbackNotDefined("Callback must be defined for digital input")
            self.__board.set_pin_mode_digital_input(pin_number=parsed_pin, callback=callback)
        elif type_ == PIN_MODE.DIGITAL_OUTPUT:
            self.__board.set_pin_mode_digital_output(pin_number=parsed_pin)
        elif type_ == PIN_MODE.PULLUP:
            if callback is None:
                raise AlimataCallbackNotDefined("Callback must be defined for pullup input")
            self.__board.set_pin_mode_digital_input_pullup(pin_number=parsed_pin, callback=callback)
        elif type_ == PIN_MODE.ANALOG_INPUT:
            if callback is None:
                raise AlimataCallbackNotDefined("Callback must be defined for analog input")
            self.__board.set_pin_mode_analog_input(pin_number=parsed_pin, callback=callback, differential=differential)
        elif type_ == PIN_MODE.ANALOG_OUTPUT:
            self.__board.set_pin_mode_analog_output(pin_number=parsed_pin)
        elif type_ == PIN_MODE.SONAR:
            if type(parsed_pin) is not list:
                raise AlimataUnexpectedPin("pin must be a list (trigger_pin, echo_pin)")
            elif callback is None:
                raise AlimataCallbackNotDefined("Callback must be defined for sonar")
            self.__board.set_pin_mode_sonar(trigger_pin=parsed_pin[0], echo_pin=parsed_pin[1], callback=callback)
        elif type_ == PIN_MODE.DHT:
            if dht_type is None:
                raise AlimataExpectedValue("dht_type is required to setup a dht")
            elif callback is None:
                raise AlimataCallbackNotDefined("Callback must be defined for dht")
            self.__board.set_pin_mode_dht(pin_number=parsed_pin, callback=callback, dht_type=dht_type)
        elif type_ == PIN_MODE.SERVO:
            self.__board.set_pin_mode_servo(pin_number=parsed_pin, min_pulse=min_pulse, max_pulse=max_pulse)
        elif type_ == PIN_MODE.STEPPER:
            if type(parsed_pin) is not list:
                raise TypeError("pin must be a list of 2 or 4 pins")
            elif stepper_type is None:
                raise AlimataExpectedValue("stepper_type is required to setup a stepper")
            # The stepper init will retrun the stepper id
            return self.__board.set_pin_mode_stepper(interface=stepper_type, pin1=parsed_pin[0], pin2=parsed_pin[1],
                                                  pin3=parsed_pin[2], pin4=parsed_pin[3], enable=True)
        elif type_ == PIN_MODE.LCD4BIT:
            # TODO MAKE BETTER PIN CHECK
            if type(parsed_pin) is not list or len(parsed_pin) != 6:
                raise TypeError("pin must be a list of pins : [rs, en, d4, d5, d6, d7]")
            self.__board.set_pin_mode_digital_output(pin_number=parsed_pin[0])
            self.__board.set_pin_mode_digital_output(pin_number=parsed_pin[1])
            self.__board.set_pin_mode_digital_output(pin_number=parsed_pin[2])
            self.__board.set_pin_mode_digital_output(pin_number=parsed_pin[3])
            self.__board.set_pin_mode_digital_output(pin_number=parsed_pin[4])
            self.__board.set_pin_mode_digital_output(pin_number=parsed_pin[5])

        elif type_ == PIN_MODE.TONE:
            self.__board.set_pin_mode_tone(pin_number=parsed_pin)
        elif type_ == PIN_MODE.I2C:
            self.__board.set_pin_mode_i2c(
                # I2C doesn't need a pin number so we use the pin parameter as the i2c port so 0 or 1
                i2c_port=parsed_pin)
        elif type_ == PIN_MODE.SPI:
            self.__board.set_pin_mode_spi(chip_select_list=parsed_pin)
        else:
            raise AlimataUnexpectedPinMode("pin mode must be from the PIN_MODE enum")

        return -1 # Return -1 if no stepper

    # Use PWM for analog write
    def write_to_pin(self, pin: Union[str, int], type_: WRITE_MODE, value: int, duration: Optional[int] = None):
        parsed_pin = self.parse_pin_number(pin=pin, type_=type_)

        # Analog OUTPUT
        if type_ == WRITE_MODE.ANALOG:
            if value >= 0 or value <= 255:
                self.__board.analog_write(pin=parsed_pin, value=value)
            elif value > 255:
                print_warning("Value is greater than 255, setting value to 255")
                self.__board.analog_write(pin=parsed_pin, value=255)
            elif value < 0:
                print_warning("Value is less than 0, setting value to 0")
                self.__board.analog_write(pin=parsed_pin, value=0)

        # Digital OUTPUT
        elif type_ == WRITE_MODE.DIGITAL:
            if value not in [0, 1]:
                raise AlimataUnexpectedValue("value for write mode digital must be equal to 0 or 1")
            else:
                self.__board.digital_write(pin=parsed_pin, value=value)
        elif type_ == WRITE_MODE.SERVO:
            self.__board.servo_write(pin_number=parsed_pin, angle=value)

        # Tone Duration OUTPUT
        elif type_ == WRITE_MODE.TONE:
            if duration is None:
                raise AlimataExpectedValue("duration (in ms) is required for tone")
            self.__board.tone(pin_number=parsed_pin, frequency=value, duration=duration)
        elif type_ == WRITE_MODE.TONE_CONTINUOUS:
            self.__board.tone(pin_number=parsed_pin, frequency=value)
        elif type_ == WRITE_MODE.TONE_STOP:
            self.__board.no_tone(pin_number=parsed_pin)
        else:
            raise AlimataUnexpectedWriteMode("type must be one of the WRITE_MODE enum")

    def i2c_communication(self, command: I2C_COMMAND, adress, i2c_port: int = 0, register=None, number_of_bytes=None,
                          args: list = None, callback=None):
        if command == I2C_COMMAND.READ:
            if number_of_bytes is None or register is None:
                raise AlimataExpectedValue("number_of_bytes and register are required to read from i2c")
            else:
                self.__board.i2c_read(address=adress, register=register, number_of_bytes=number_of_bytes,
                                      callback=callback, i2c_port=i2c_port)
        elif command == I2C_COMMAND.WRITE:
            if args is None:
                raise AlimataExpectedValue("args are required to write to i2c")
            else:
                self.__board.i2c_write(address=adress, args=args, i2c_port=i2c_port)
        elif command == I2C_COMMAND.READ_RESTART_TRANSMISSION:
            if number_of_bytes is None or register is None:
                raise AlimataExpectedValue("number_of_bytes and register are required to read from i2c")
            else:
                self.__board.i2c_read_restart_transmission(address=adress, register=register,
                                                           number_of_bytes=number_of_bytes, callback=callback,
                                                           i2c_port=i2c_port)
        else:
            raise AlimataUnexpectedI2cCommand("command must be one of the I2C_COMMAND enum")

    def spi_communication(self, command: SPI_COMMAND, cs_pin: Union[int, str], _bytes: list = None, register=None,
                          number_of_bytes=None, callback=None):
        parsed_cs_pin = self.parse_pin_number(pin=cs_pin, type_=PIN_MODE.SPI)
        self.__board.spi_cs_control(chip_select_pin=parsed_cs_pin, select=0)  # Select the device

        if command == SPI_COMMAND.WRITE_BLOCKING:
            if _bytes is None:
                raise AlimataExpectedValue("bytes are required to write to spi")
            self.__board.spi_write_blocking(_bytes)
        elif command == SPI_COMMAND.READ_BLOCKING:
            if number_of_bytes is None:
                raise AlimataExpectedValue("number_of_bytes is required to read from spi")
            if register is None:
                raise AlimataExpectedValue("register is required to read from spi")
            self.__board.spi_read_blocking(register_selection=register, number_of_bytes_to_read=number_of_bytes,
                                           call_back=callback)
        elif command == SPI_COMMAND.SET_FORMAT:
            # TODO: Implement this
            raise NotImplementedError("SPI set format not implemented yet")

        self.__board.spi_cs_control(chip_select_pin=parsed_cs_pin, select=1)  # Deselect the device

    @property
    def firmetix_board(self):
        return self.__board
