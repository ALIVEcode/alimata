"""
A core set of feature to simplify the use of pymata_express and asyncio
"""
from pymata_express import pymata_express
import asyncio
from enum import Enum


def is_async_function(func):
    return asyncio.iscoroutinefunction(func)


def maprange(value: int | float, from_min: int | float, from_max: int | float, to_min: int | float, to_max: int | float):
    return to_min + ((value - from_min) * (to_max - to_min) / (from_max - to_min))

def print_warning(message: str = ""):
    print("Warning : ", message)


class PIN_MODE(str, Enum):
    INPUT = "INPUT"
    OUTPUT = "OUTPUT"
    PULLUP = "PULLUP"
    ANALOG = "ANALOG"
    PWM = "PWM"
    SONAR = "SONAR"
    DHT = "DHT"
    SERVO = "SERVO"
    STEPPER = "STEPPER"
    TONE = "TONE"

class DHT_SENSOR_TYPE(int, Enum):
    DHT11 = 11
    DHT12 = 12
    DHT22 = 22
    DHT21 = 21
    # AM2301 = "AM2301"


class WRITE_MODE(str, Enum):
    PWM = "PWM"
    DIGITAL = "DIGITAL"
    TONE = "TONE"
    TONE_CONTINUOUS = "TONE_CONTINUOUS"
    TONE_STOP = "TONE_STOP"
    SERVO = "SERVO"
    STEPPER = "STEPPER"
