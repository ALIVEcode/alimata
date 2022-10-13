from alimata.core.board import Board
from alimata.core.core import PIN_MODE, WRITE_MODE, maprange, print_warning
from alimata.actuators.actuator import Actuator
import asyncio


class Led(Actuator):

    # Toggle the led on or off
    # Intensity should be bettewn 0 and 100
    async def toggle(self, intensity: int = 100):
        new_status = 1 - self.__status
        await self.set_status(new_status, intensity)

    # Set the status of the led
    # Intensity should be bettewn 0 and 100
    async def set_status(self, status: int, intensity: int = 100):
        self.__status = status
        if self.__status == 0:
            await self.board.write_to_pin(self.pin, WRITE_MODE.DIGITAL, 0)
        elif intensity >= 0 and intensity < 100:
            intensity_mapped = int(maprange(intensity, 0, 100, 0, 255))
            await self.board.write_to_pin(self.pin, WRITE_MODE.PWM, intensity_mapped)
        elif intensity > 100:
            print_warning("Intensity is greater than 100, setting intensity to 100")
            await self.board.write_to_pin(self.pin, WRITE_MODE.DIGITAL, 1)
        elif intensity < 0:
            print_warning("Intensity is less than 0, setting intensity to 0")
            await self.board.write_to_pin(self.pin, WRITE_MODE.DIGITAL, 0)

    # Set the pin of the led
    # call this method if you initialize the class in an async function
    async def async_init(self):
        await self.board.set_pin_mode(self.pin, PIN_MODE.PWM)

    def __init__(self, board: Board, pin):
        self.board = board
        self.pin = pin
        self.__status = 1

        # set the event loop
        self.loop = asyncio.get_event_loop()

        # Start the async init
        self.loop.run_until_complete(self.async_init())
