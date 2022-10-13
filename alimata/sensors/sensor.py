from pymata_express import pymata_express


class Sensor:

    def __init__(self, board: pymata_express.PymataExpress) -> None:
        self.board = board
