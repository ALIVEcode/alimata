from hashlib import new
from alimata.actuators.led import Led
from alimata.core.board import Board
from alimata.core.core import PIN_MODE, WRITE_MODE
from alimata.actuators.actuator import Actuator
import asyncio

class LedRGB(Led):

    def __init__(self, board: Board, pin):
        super().__init__(board, pin)
        self.__status = False
        self.__intensity = 255
        self.__redLvl = 255
        self.__greenLvl = 255
        self.__blueLvl = 255

    
    def toggle(self):
        return super().toggle()

    def on(self):
        return super().on()

    def off(self):
        return super().off()

    @property
    def intensity(self):
        return super().intensity
    
    @intensity.setter
    async def intensity(self):
        return super().intensity

    @property
    def greenLevel(self):
        """
        Get or Set the value of the green [0-255]\n
        """
        return self.__greenLvl
     
    @greenLevel.setter
    async def greenLevel(self, greenLvl: int):
        """
        Get or Set the value of the green [0-255]\n
        """        
        self.__greenLvl = greenLvl
        await self.board.write_to_pin(self.pin, WRITE_MODE.PWM, greenLvl)

    @property
    def redLevel(self):
        """
        Get or Set the value of the red [0-255]\n
        """
        return self.__redLvl
     
    @redLevel.setter
    async def redLevel(self, redLvl: int):
        """
        Set the value of the red [0-255]\n
        """        
        self.__redLvl = redLvl
        await self.board.write_to_pin(self.pin, WRITE_MODE.PWM, redLvl)

    @property
    def blueLevel(self):
        """
        Get or Set the value of the blue [0-255]\n
        """
        return self.__blueLvl
     
    @redLevel.setter
    async def bluevel(self, blueLvl: int):
        """
        Set the value of the blue [0-255]\n
        """        
        self.__blueLvl = blueLvl
        await self.board.write_to_pin(self.pin, WRITE_MODE.PWM, blueLvl)
