from alimata.core.board import Board
from alimata.core.core import PIN_MODE, WRITE_MODE
from alimata.actuators.actuator import Actuator



class Led(Actuator):
    """
    A class used to represent a Led

    Attributes
    ----------
    data : bool
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
        Actuator.__init__(self, board=board, pin=pin, type=PIN_MODE.PWM)
        self._Actuator__data = False


    def toggle(self):
        """
        Toggle the led on or off \n
        """
        if self._Actuator__data:
            self.off(self)
        else:
            self.on(self)

    
    def on(self):
        """
        Turn the led on \n
        """
        self._Actuator__data = True
        self.board.write_to_pin(self.pin, WRITE_MODE.PWM, self.__intensity)
        # await self.board.write_to_pin(self.pin, WRITE_MODE.PWM, 255)
    
    def off(self):
        """
        Turn the led off \n
        """
        self._Actuator__data = False
        self.board.write_to_pin(self.pin, WRITE_MODE.PWM, 0)



    @property
    def intensity(self):
        """
        Get or Set the intensity of the led [0-255]\n
        """
        return self.__intensity
       
     
    @intensity.setter
    def intensity(self, intensity: int):
        self.__intensity = intensity
        self.board.write_to_pin(self.pin, WRITE_MODE.PWM, intensity)

  

    @property
    def data(self):
        """
        Get or Set the current status of the led [True/False]\n
        """
        return self._Actuator__data
    
    @data.setter
    def data(self, status: bool):
        self._Actuator__data = status
        if status:
            self.on()
        else:
            self.off()