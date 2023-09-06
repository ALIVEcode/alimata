class AlimataUnexpectedError(Exception):
    def __init__(self, msg: str):
        super().__init__(msg)


class AlimataUnexpectedPin(Exception):
    def __init__(self, msg: str):
        super().__init__("Unexpected pin number ", msg)


class AlimataUnexpectedPinMode(Exception):
    def __init__(self, msg: str):
        super().__init__("Unexpected pin mode ", msg)


class AlimataUnexpectedWriteMode(Exception):
    def __init__(self, msg: str):
        super().__init__("Unexpected write mode ", msg)


class AlimataUnexpectedValue(Exception):
    def __init__(self, msg: str):
        super().__init__("Unexpected value ", msg)


class AlimataExpectedValue(Exception):
    def __init__(self, msg: str):
        super().__init__("Expected value ", msg)


class AlimataUnexpectedI2cCommand(Exception):
    def __init__(self, msg: str):
        super().__init__("Unexpected I2C command ", msg)

class AlimataExpectedParameters(Exception):
    def __init__(self, msg: str):
        super().__init__("Expected parameters ", msg)


class AlimataCallbackNotDefined(Exception):
    def __init__(self, msg: str):
        super().__init__("Callback not defined ", msg)
