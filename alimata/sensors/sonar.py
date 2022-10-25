from alimata.core.core import PIN_MODE
from alimata.core.board import Board
from alimata.sensors.sensor import Sensor


class Sonar(Sensor):

   
    # Is called when the sensor changes value
    async def _value_changed_callback(self, data):
        self.__value = data[2]

        if self.__callback is not None:
            self.__callback(data)

    def __init__(self, board: Board.board, trigger_pin, echo_pin, callback=None):

        super().__init__(board=board, pin=trigger_pin, callback=callback, type_=PIN_MODE.SONAR, echo_pin=echo_pin)

    @property
    def data(self):
        """Return the current distance of the sensor"""
        return self._Sensor__data
    
    @property
    def distance(self):
        """Return the current distance of the sensor"""
        return self._Sensor__data

    def _Sensor__is_changed_callback(self, data):
        """Callback when the sensor's data has changed enough"""
        try:
            if self.board.is_started:
                self._Sensor__data = data[2]
                if Sensor.is_ready(self) and self._Sensor__callback is not None:
                    self._Sensor__callback(self)
        except Exception as e:
            print(e)


