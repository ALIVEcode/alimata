"""
A core set of feature to simplify the use of pymata_express and asyncio
"""
from enum import Enum
from typing import Union


def map_range(value: Union[float, int], from_min: Union[float, int], from_max: Union[float, int],
              to_min: Union[float, int], to_max: Union[float, int]) -> Union[float, int]:
    ''' Map a value from a range to another range '''
    return to_min + ((value - from_min) * (to_max - to_min) / (from_max - to_min))


def normalize_angle(angle: int) -> int:
    '''Normalize the angle to be between 0 and 180'''
    if angle > 180:
        print_warning("Angle > 180, setting to 180")
        return 180
    elif angle < 0:
        print_warning("Angle < 0, setting to 0")
        return 0
    else:
        return angle


def print_warning(message: str = ""):
    print("Warning : ", message)


class PIN_MODE(str, Enum):
    DIGITAL_INPUT = "DIGITAL_INPUT"
    DIGITAL_OUTPUT = "DIGITAL_INPUT"
    PULLUP = "PULLUP"
    ANALOG_INPUT = "ANALOG_INPUT"
    ANALOG_OUTPUT = "ANALOG_OUTPUT"
    SONAR = "SONAR"
    DHT = "DHT"
    SERVO = "SERVO"
    STEPPER = "STEPPER"
    TONE = "TONE"
    I2C = "I2C"
    SPI = "SPI"
    LCD4BIT = "LCD4BIT"


class WRITE_MODE(str, Enum):
    ANALOG = "ANALOG"
    DIGITAL = "DIGITAL"
    SERVO = "SERVO"
    TONE = "TONE"
    TONE_CONTINUOUS = "TONE_CONTINUOUS"
    TONE_STOP = "TONE_STOP"


class DHT_TYPE(int, Enum):
    DHT11 = 11
    DHT22 = 22


class STEPPER_TYPE(int, Enum):
    STEPPER = 1
    FULL2WIRE = 2
    FULL3WIRE = 3
    FULL4WIRE = 4
    HALF3WIRE = 6
    HALF4WIRE = 8


class I2C_COMMAND(str, Enum):
    READ = "READ"
    READ_CONTINUOUS = "READ_CONTINUOUS"
    READ_RESTART_TRANSMISSION = "READ_RESTART_TRANSMISSION"
    WRITE = "WRITE"


class SPI_COMMAND(str, Enum):
    READ_BLOCKING = "READ_BLOCKING"
    WRITE_BLOCKING = "WRITE_BLOCKING"
    SET_FORMAT = "SET_FORMAT"

class CONNECTION_TYPE(int, Enum):
    SERIAL = 0
    WIFI = 1
    BLUETOOTH = 2
