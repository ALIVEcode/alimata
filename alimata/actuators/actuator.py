from pymata_express import pymata_express


class Actuator:

    def __init__(self, board: pymata_express.PymataExpress) -> None:
        self.board = board
