# dvl-serial Python library to serial interface with Water Linked DVLs
Python code to serial interface with Water Linked DVLs.

The library makes setting up a serial connection with the DVL simpler. Handles the parsing, checks validity and returns a Dictionary.

## Resources

* [Water Linked web site](https://waterlinked.com/dvl/)
* [DVL A50 documentation](https://waterlinked.github.io/dvl/dvl-a50/)
* [DVL protocol specification](https://waterlinked.github.io/dvl/dvl-protocol/)
* [Repository](https://github.com/waterlinked/dvl-serial)

## Requirements

* Python 3.*
* crcmod
```bash
pip install crcmod
```
You might also need additional permission to access the port on the system you're running the script

## Supported DVLs

* Water Linked DVL A50

## Setup

Download or clone the repo to the base of your project.
```bash
cd /project_location
git clone https://github.com/waterlinked/dvl-serial.git
```

## Quick start

Connecting to a dvl and reading data:

```py
$ python3

>>>  from wldvl import WlDVL
>>>  dvl = WlDVL("/dev/ttyUSB0")
>>>  dvl.read()
{'c': 'x', 'dir': 'RESP', 'options': {'fom': 0.002, 'time': 40.57, 'vy': 0.004, 'vz': -0.002, 'vx': -0.003, 'valid': True, 'altitude': 0.14}}
```

## Usage

The `WlDVL` class provides an easy interface to receive data with a Water Linked DVL.

A `WlDVL` object is initialized with the serial device port:

```py
from wldvl import WlDVL
dvl = WlDVL("/dev/ttyUSB0")
```
To retrieve data as a dictionary:
```py
dvl.read()
```

This should give you a dictionary formated as follows:
```json
{
    'dir': 'RESP',
    'c': 'x',
    'options': {
        'time': 40.75,
        'vx': 0.001,
        'vy': 0.004,
        'vz': -0.001,
        'fom': 0.002,
        'altitude': 0.13,
        'valid': True
    }
}
```

## Examples

Examples showing how to use the API is available in the [example/](example/) folder.
