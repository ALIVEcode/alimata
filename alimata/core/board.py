import imp
from alimata.core.core import PIN_MODE, WRITE_MODE, DHT_SENSOR_TYPE, print_warning
from alimata.core.error import AlimataUnexpectedPin
from pymata_express import pymata_express
import asyncio, sys, datetime


class Board:
    """
    A class used to represent the arduino board

    Attributes
    ----------
    board_id : int
        The id of the board same as in firmata (read only)

    
    Methods
    ---------
    start(setup_func, loop_func)
        Starting the board : (setup_func, loop_func)
    is_started : bool
        Retuns if the board is started or not (read only)
    pymata_board : pymata_express
        The pymata_express board object (read only)
    set_pin_mode : function
        Setting the pin mode : (pin, type, callback=None, differential=1, echo_pin=None, timeout=8000, sensor_type=None, min_pulse=544, max_pulse=2400, step_per_revolution=None)
    write_pin : function
        Writing to a pin : (pin, type, value, duration, step)
    parse_pin_number : function
        Converting the analog pin value to the correct one depending on the board and function used : (pin, pin_type)
    
    """

    def __init__(self, board_id: int = 1, COM_port=None, baud_rate=115200):
        self.__board = pymata_express.PymataExpress(arduino_instance_id=board_id, com_port=COM_port, baud_rate=baud_rate, arduino_wait=2)
        self.__board_id = board_id
        self.__is_started = False
        self.__num_of_digital_pins = len(self.__board.digital_pins)
        self.__num_of_analog_pins = len(self.__board.analog_pins)

        # get the event loop
        self.__loop = asyncio.get_event_loop()

    async def __main(self):
        # start the setup function
        await self.__setup_func()

        
        self.__is_started = True

        # loop the loop function
        while self.__is_started:
            await self.__loop_func()

    def start(self, setup_func, loop_func):
        if self.__is_started == True:
            print_warning("Board is already started, not starting again")
        else:

            # saving the functions
            self.__setup_func = setup_func
            self.__loop_func = loop_func


            try:
                # start the main function
                self.__loop.run_until_complete(self.__main())

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
        tasks = asyncio.all_tasks()
        for t in tasks:
            t.cancel()

        print("SHUTING DOWN BOARD ! | ID : " + str(self.__board_id) + " | TIME : " + str(datetime.datetime.now().strftime("%H:%M:%S")))
        self.__loop.run_until_complete(self.__board.shutdown())

    
    # Converting the analog pin value to the correct one depending on the board and function used
    def parse_pin_number(self, pin: str | int, pin_type) -> int:
        if type(pin) == str:
            if pin.startswith("A"): #Check if it's an analog pin
                pin = pin[1:]
                if pin_type != "ANALOG":
                    pin = int(pin) + self.__num_of_digital_pins
        return int(pin)


    async def set_pin_mode(self, pin: str | int, type_: PIN_MODE, callback=None, differential: int = 1, echo_pin: str | int = None, timeout: int = 8000, sensor_type: DHT_SENSOR_TYPE = None, min_pulse: int = 544, max_pulse:int =2400, step_per_revolution: int = None):
        pin = self.parse_pin_number(pin, type_)
        
        if type_ == PIN_MODE.INPUT:
            await self.__board.set_pin_mode_digital_input(pin, callback)
        elif type_ == PIN_MODE.OUTPUT:
            await self.__board.set_pin_mode_digital_output(pin)
        elif type_ == PIN_MODE.PULLUP:
            await self.__board.set_pin_mode_digital_input_pullup(pin, callback)
        elif type_ == PIN_MODE.ANALOG:
            await self.__board.set_pin_mode_analog_input(pin, callback, differential)
        elif type_ == PIN_MODE.PWM:
            await self.__board.set_pin_mode_pwm_output(pin)
        elif type_ == PIN_MODE.SONAR:
            if echo_pin is None:
                raise TypeError("echo_pin is required to setup a sonar")
            else:
                await self.__board.set_pin_mode_sonar(pin, echo_pin, callback, timeout)
        elif type_ == PIN_MODE.DHT:
            if sensor_type is None:
                raise TypeError("sensor_type is required to setup a DHT sensor")
            else:
                await self.__board.set_pin_mode_dht(pin, sensor_type, differential, callback)
        elif type_ == PIN_MODE.SERVO:
            await self.__board.set_pin_mode_servo(pin, min_pulse, max_pulse)
        elif type_ == PIN_MODE.STEPPER:
            if step_per_revolution is None:
                raise TypeError("step_per_revolution is required to setup a stepper motor")
            elif len(pin) != 2 or len(pin) != 4:
                raise TypeError("pin must be a list of 2 or 4 pins")
            else:
                await self.__board.set_pin_mode_stepper(step_per_revolution, pin)
        elif type_ == PIN_MODE.TONE:
            await self.__board.set_pin_mode_tone(pin)
        else:
            raise TypeError("type must be INPUT, OUTPUT, PULLUP, ANALOG, PWM or SONAR")

        
    # Use PWM for analog write
    def write_to_pin(self, pin: str | int, type: WRITE_MODE, value: int, duration: int = 500, step: int = 1):
        pin = self.parse_pin_number(pin, type)

        if type == WRITE_MODE.PWM:
            if value >= 0 or value <= 255:
                asyncio.create_task(self.__board.pwm_write(pin, value))
            elif value > 255:
                print_warning("Value is greater than 255, setting value to 255")
                asyncio.create_task(self.__board.pwm_write(pin, 255))
            elif value < 0:
                print_warning("Value is less than 0, setting value to 0")
                asyncio.create_task(self.__board.pwm_write(pin, 0))
        elif type == WRITE_MODE.DIGITAL:
            if value not in [0, 1]:
                raise TypeError("value must be equal to 0 or 1")
            else:
                asyncio.create_task( self.__board.digital_write(pin, value))
        elif type == WRITE_MODE.TONE:
            asyncio.create_task(self.__board.play_tone(pin, value, duration))
        elif type == WRITE_MODE.TONE_CONTINUOUS:
            asyncio.create_task(self.__board.play_tone_continuously(pin, value))
        elif type == WRITE_MODE.TONE_STOP:
            asyncio.create_task(self.__board.stop_tone(pin))
        elif type == WRITE_MODE.SERVO:
            asyncio.create_task(self.__board.servo_write(pin, value))
        elif type == WRITE_MODE.STEPPER:
            asyncio.create_task(self.__board.stepper_write(value, step))
        else:
            raise TypeError("type must be ANALOG, PWM, DIGITAL, TONE, TONE_CONTINUOUS, TONE_STOP, SERVO or STEPPER")
    
    @property
    def pymata_board(self):
        return self.__board