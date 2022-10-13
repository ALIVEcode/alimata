"""
A core set of feature to simplify the use of pymata_express and asyncio
"""
from pymata_express import pymata_express
import asyncio
from enum import Enum


def is_async_function(func):
    return asyncio.iscoroutinefunction(func)


def maprange(value: int, from_min: int, from_max: int, to_min: int, to_max: int):
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


class WRITE_MODE(str, Enum):
    PWM = "PWM"
    DIGITAL = "DIGITAL"
    TONE = "TONE"
    TONE_CONTINUOUS = "TONE_CONTINUOUS"
    TONE_STOP = "TONE_STOP"
    SERVO = "SERVO"
    STEPPER = "STEPPER"
