from alimata.core.core import PIN_MODE, WRITE_MODE, DHT_SENSOR_TYPE, print_warning
from pymata_express import pymata_express
import asyncio, sys


class Board:

    def __init__(self, board_id: int = 1, COM_port=None, baud_rate=115200):
        self.__board = pymata_express.PymataExpress(arduino_instance_id=board_id, com_port=COM_port, baud_rate=baud_rate, arduino_wait=2)
        self.board_id = board_id
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
        while True:
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
                self.__loop.run_until_complete(self.shutdown())
                sys.exit(0)

    @property
    def is_started(self):
        return self.__is_started

    async def shutdown(self):
        await self.__board.shutdown()

    
    # Converting the analog pin value to the correct one depending on the board and function used
    def parse_pin_number(self, pin: str, pin_type):
        if pin.startswith("A"): #Check if it's an analog pin
            pin = pin[1:]
            if pin_type != "ANALOG":
                pin = int(pin) + self.__num_of_digital_pins
        return int(pin)


    async def set_pin_mode(self, pin: str, type: str, callback=None, differential: int = 1, echo_pin: str = None, timeout: int = 8000,
                           sensor_type: int = None, min_pulse: int = 544, max_pulse:int =2400, step_per_revolution: int = None):
        pin = self.parse_pin_number(str(pin), type)

        if type == "INPUT":
            await self.__board.set_pin_mode_digital_input(pin, callback)
        elif type == "OUTPUT":
            await self.__board.set_pin_mode_digital_output(pin)
        elif type == "PULLUP":
            await self.__board.set_pin_mode_digital_input_pullup(pin, callback)
        elif type == "ANALOG":
            await self.__board.set_pin_mode_analog_input(pin, callback, differential)
        elif type == "PWM":
            await self.__board.set_pin_mode_pwm_output(pin)
        elif type == "SONAR":
            if echo_pin is None:
                raise TypeError("echo_pin is required to setup a sonar")
            else:
                await self.__board.set_pin_mode_sonar(pin, echo_pin, callback, timeout)
        elif type == "DHT":
            if sensor_type is None:
                raise TypeError("sensor_type is required to setup a DHT sensor")
            else:
                await self.__board.set_pin_mode_dht(pin, sensor_type, differential, callback)
        elif type == "SERVO":
            await self.__board.set_pin_mode_servo(pin, min_pulse, max_pulse)
        elif type == "STEPPER":
            if step_per_revolution is None:
                raise TypeError("step_per_revolution is required to setup a stepper motor")
            elif len(pin) != 2 or len(pin) != 4:
                raise TypeError("pin must be a list of 2 or 4 pins")
            else:
                await self.__board.set_pin_mode_stepper(step_per_revolution, pin)
        elif type == "TONE":
            await self.__board.set_pin_mode_tone(pin)
        else:
            raise TypeError("type must be INPUT, OUTPUT, PULLUP, ANALOG, PWM or SONAR")

        
    # Use PWM for analog write
    def write_to_pin(self, pin, type: str, value: int, duration: int = 500, step: int = 1):
        pin = self.parse_pin_number(str(pin), type)

        if type == "PWM":
            if value >= 0 or value <= 255:
                asyncio.create_task(self.__board.pwm_write(pin, value))
            elif value > 255:
                print_warning("Value is greater than 255, setting value to 255")
                asyncio.create_task(self.__board.pwm_write(pin, 255))
            elif value < 0:
                print_warning("Value is less than 0, setting value to 0")
                asyncio.create_task(self.__board.pwm_write(pin, 0))
        elif type == "DIGITAL":
            if value not in [0, 1]:
                raise TypeError("value must be equal to 0 or 1")
            else:
                asyncio.create_task( self.__board.digital_write(pin, value))
        elif type == "TONE":
            asyncio.create_task(self.__board.play_tone(pin, value, duration))
        elif type == "TONE_CONTINUOUS":
            asyncio.create_task(self.__board.play_tone_continuously(pin, value))
        elif type == "TONE_STOP":
            asyncio.create_task(self.__board.stop_tone(pin))
        elif type == "SERVO":
            asyncio.create_task(self.__board.servo_write(pin, value))
        elif type == "STEPPER":
            asyncio.create_task(self.__board.stepper_write(pin, value, step))
        else:
            raise TypeError("type must be ANALOG, PWM, DIGITAL, TONE, TONE_CONTINUOUS, TONE_STOP, SERVO or STEPPER")
    
    @property
    def pymata_board(self):
        return self.__board