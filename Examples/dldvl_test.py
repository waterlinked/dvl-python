from wldvl import WlDVL

dvl = WlDVL("/dev/ttyUSB0")
#dvl.read()
x = dvl.read()
print(x)

print(x['options']['time'])
#dvl.get_data_packet()