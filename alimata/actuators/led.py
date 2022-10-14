from alimata.core.board import Board
from alimata.core.core import PIN_MODE, WRITE_MODE
from alimata.actuators.actuator import Actuator
import asyncio



class Led(Actuator):
    """
    A class used to represent a Led

    Attributes
    ----------
    status : bool
        the status of the led (on or off)
    intensity : int
        the intensity of the led (0-255)

    Methods
    -------
    toggle()
        Toggle the led on or off
    on()
        Turn the led on
    off()
        Turn the led off
    """
    def __init__(self, board: Board, pin):
        self.board = board
        self.pin : str = pin
        self.__status : bool = True
        self.__intensity : int = 255

        # set the event loop
        self.loop = asyncio.get_event_loop()

        
        # Start the async init
        self.loop.run_until_complete(self.async_init())

    # Set the pin of the led
    # call this method if you initialize the class in an async function
    async def async_init(self):
        await self.board.set_pin_mode(self.pin, PIN_MODE.PWM)


    async def toggle(self):
        """
        Toggle the led on or off \n
        """
        if self.__status:
            await self.off(self)
        else:
            await self.on(self)

    
    async def on(self):
        """
        Turn the led on \n
        """
        self.__status = True
        await self.board.write_to_pin(self.pin, WRITE_MODE.PWM, 255)
    
    async def off(self):
        """
        Turn the led off \n
        """
        self.__status = False
        await self.board.write_to_pin(self.pin, WRITE_MODE.PWM, 0)



    @property
    def intensity(self):
        """
        Get or Set the intensity of the led [0-255]\n
        """
        return self.__intensity
       
     
    @intensity.setter
    async def intensity(self, intensity: int):
        self.__intensity = intensity
        await self.board.write_to_pin(self.pin, WRITE_MODE.PWM, intensity)

  

    @property
    def status(self):
        """
        Get or Set the current status of the led [True/False]\n
        """
        return self.__status
    
    @status.setter
    async def status(self, status: bool):
        self.__status = status
        if status:
            await self.on()
        else:
            await self.off()