from wldvl import WlDVL

dvl = WlDVL("/dev/ttyUSB0")
x = dvl.read()
print(x)

#Parsing the time value from the serial data can be done as the following
print(x['options']['time'])
