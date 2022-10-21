from alimata.sensors.dht import DHT
from alimata.core.board import Board
from asyncio import sleep


#Creating a new board
board = Board()


def callback_func(sensor):
    print("SENSOR UPDATED ! | PIN : " + str(sensor.pin))
    pass


dhtPin = 5

dht = DHT(board, dhtPin)



#Main function
async def setup():
    print("Starting main")


async def loop():
    if dht.is_ready():
        temp = dht.temperature
        hum = dht.humidity
        print("Temp : " + str(temp) + " | Humidity : " + str(hum))



    await sleep(1)

board.start(setup, loop)