# Alimata

## What is it?

Alimata is a python library used to simplify the implementation of [pymata-express](https://mryslab.github.io/pymata-express/) library

## Requirements

- python 3.7 or higher
- telemetrix
- Telemtrix4Arduino

## Installing

### Telemetrix

To install Telemetrix on Linux (including Raspberry Pi) and macOS computers, open a terminal window and type: `sudo pip3 install telemetrix`

For Windows users type: `pip install telemetrix`

### Telemtrix4Arduino

1. Open the Arduino IDE and select Tools/Manage Libraries
2. Search for "Telemtrix4Arduino"
3. Install
4. Telemtrix4Arduino also requires other library just install all of them.
5. Open the Telemtrix4Arduino example
6. If you plan to use multiple arduino use `#define ARDUINO_INSTANCE_ID 1`
7. Flash it to the arduino

## Code structure

### Board

Creating a new board
`board = Board()`

Making the setup and loop function and starting the board

```python
    async def setup():
        #Code here is run once

    async def loop():
        #Code here is run in a loop

    #Starting the board by passing the setup and loop function
    board.start(setup,loop)

    #Shuting the board down
    board.shutdown()
```

#### All options of the board

```python
    #Create the new board (optional board_id and COM_port)
    board = Board(board_id, COM_port)

    #Starting the board setup and loop async function
    board.start(setup,loop)

    #Use to set the pin mode with the type (INPUT, OUTPUT, ANALOG, PWM, SONAR)
    board.set_pin_mode(pin, type, callback, differential, echo_pin, timeout, sensor_type, min_pulse, max_pulse)

    #Use to write to a pin with the type (ANALOG, PWM, DIGITAL, TONE, TONE_CONTINUOUS, TONE_STOP, SERVO, STEPPER)
    board.write_pin(pin, value, type, duration, step)
```

### Sensors

Creating a new sensor object (button in this case)
`button1 = Button(board, 2)`

### Actuators

Creating a new actuator object (led in this case)
`led1 = Led(board, 3)`
