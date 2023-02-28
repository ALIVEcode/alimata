from alimata.sensors.dht import DHT
from alimata.core.board import Board
from alimata.core.core import DHT_TYPE
from time import sleep

# Creating a new board
board = Board()


def callback_func(obj):
    print("SENSOR UPDATED ! | PIN : " + str(obj.pin))
    pass


dhtPin = 5

dht = DHT(board, dhtPin, DHT_TYPE.DHT11)


# Main function
def setup():
    print("Starting main")


def loop():
    if dht.is_ready():
        temp = dht.temperature
        hum = dht.humidity
        print("Temp : " + str(temp) + " | Humidity : " + str(hum))

    sleep(1)


board.start(setup, loop)
