from alimata.core.core import PIN_MODE, WRITE_MODE, print_warning
from pymata_express import pymata_express
import asyncio, sys


class Board:

    def __init__(self, board_id: int = 1, COM_port=None, baud_rate=115200):
        self.__board = pymata_express.PymataExpress(arduino_instance_id=board_id, com_port=COM_port,
                                                    baud_rate=baud_rate)
        self.board_id = board_id
        self.__is_started = False
        self.__num_of_digital_pins = len(self.__board.digital_pins)
        self.__num_of_digital_pins = len(self.__board.analog_pins)

    async def __main(self):
        # start the setup function
        await self.__setup()

        # loop the loop function
        while True:
            await self.__loop()

    def start(self, setup, loop):
        if self.__is_started == True:
            print_warning("Board is already started, not starting again")
        else:
            self.__is_started = True

            # saving the functions
            self.__setup = setup
            self.__loop = loop

            # get the event loop
            loop = asyncio.get_event_loop()

            try:
                # start the main function
                loop.run_until_complete(self.__main())

            except (KeyboardInterrupt, RuntimeError) as e:
                loop.run_until_complete(self.shutdown())
                sys.exit(0)

    async def shutdown(self):
        self.__board.shutdown()

    
    # Converting the analog pin value to the correct one depending on the board and function used
    async def parse_pin_number(self, pin: str, pin_type):
        if pin.startswith("A"): #Check if it's an analog pin
            pin = pin[1:]
            if pin_type != "ANALOG":
                pin = int(pin) + self.__num_of_digital_pins
        return int(pin)


    async def set_pin_mode(self, pin: str, type: str, callback=None, differential=1, echo_pin=None, timeout=8000,
                           sensor_type="DHT11", min_pulse=544, max_pulse=2400):
        pin = await self.parse_pin_number(str(pin), type)

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
        else:
            raise TypeError("type must be INPUT, OUTPUT, PULLUP, ANALOG, PWM or SONAR")

        
    # Use PWM for analog write
    async def write_to_pin(self, pin, type: str, value: int, duration: int = 500, step: int = 1):
        pin = await self.parse_pin_number(str(pin), type)

        if type == "PWM":
            if value >= 0 or value <= 255:
                await self.__board.pwm_write(pin, value)
            elif value > 255:
                print_warning("Value is greater than 255, setting value to 255")
                await self.__board.pwm_write(pin, 255)
            elif value < 0:
                print_warning("Value is less than 0, setting value to 0")
                await self.__board.pwm_write(pin, 0)
        elif type == "DIGITAL":
            if value not in [0, 1]:
                raise TypeError("value must be equal to 0 or 1")
            else:
                await self.__board.digital_write(pin, value)
        elif type == "TONE":
            await self.__board.play_tone(pin, value, duration)
        elif type == "TONE_CONTINUOUS":
            await self.__board.play_tone_continuously(pin, value)
        elif type == "TONE_STOP":
            await self.__board.stop_tone(pin)
        elif type == "SERVO":
            await self.__board.servo_write(pin, value)
        elif type == "STEPPER":
            await self.__board.stepper_write(pin, value, step)
        else:
            raise TypeError("type must be ANALOG, PWM, DIGITAL, TONE, TONE_CONTINUOUS, TONE_STOP, SERVO or STEPPER")