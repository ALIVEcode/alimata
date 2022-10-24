class AlimataUnexpectedError(Exception):
    def __init__(self, msg: str):
        super().__init__(msg)

class AlimataUnexpectedPin(Exception):
    def __init__(self, msg: str):
        super().__init__("Unexpected pin number ", msg)