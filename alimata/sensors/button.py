from alimata.core.core import is_async_function, PIN_MODE
from alimata.sensors.sensor import Sensor
from alimata.core.board import Board


class Button(Sensor):
    """
    A class used to represent a Button

    Attributes
    ----------
    value : bool
        the value of the Button (Pressed or Released)
    pin : str
        the pin of the Button
    invert : bool
        if the button is inverted or not
    """

    def __init__(self, board: Board, pin: str, invert: bool = False, callback=None):
        
        Sensor.__init__(self, board=board, pin=pin, callback=callback, type=PIN_MODE.PULLUP)

        self.invert = invert



    @property
    def data(self):
        """Return the current status of the button (True or False)"""
        return self._Sensor__data


    # Change the status of the button when pressed
    async def _Sensor__is_changed_callback(self, data):
        try:
            if self.board.is_started:
                if self.invert:
                    self._Sensor__data = not bool(data[2])
                else:
                    self._Sensor__data = bool(data[2])
                if Sensor.is_ready(self) and self._Sensor__callback is not None:
                    if is_async_function(self._Sensor__callback):
                        await self._Sensor__callback(self)
                    else:
                        self._Sensor__callback(self)
        except Exception as e:
            print(e)
