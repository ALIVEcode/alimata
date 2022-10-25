"""
A core set of feature to simplify the use of pymata_express and asyncio
"""
from enum import Enum
from typing import Union


def maprange(value: Union[str, int], from_min: Union[str, int], from_max: Union[str, int], to_min: Union[str, int], to_max: Union[str, int]):
    return to_min + ((value - from_min) * (to_max - to_min) / (from_max - to_min))

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
    SERVO_DETATCH = "SERVO_DETATCH"

class WRITE_MODE(str, Enum):
    ANALOG = "ANALOG"
    DIGITAL = "DIGITAL"
    SERVO = "SERVO"
    STEPPER = "STEPPER"
