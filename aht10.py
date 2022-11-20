import utime
import sys
import machine

#---- CONSTANTS --------------------------------------------------------------

TP_ADDR = 0x38 
TP_INIT = 0xE1
TP_READ = 0xAC

# float precision
PRECISION = 2
#-----------------------------------------------------------------------------

# read from the I2C bus, stopping after the nbytes
def bus_read(i2c, addr, nbytes=1):
    if nbytes < 1:
        return bytearray()   
    data = i2c.readfrom(addr, nbytes)
    return data

# wirte on the I2C bus
def bus_write(i2c, addr, data):
    msg = bytearray()
    msg.append(data)
    i2c.writeto(addr, msg)

def read_values(i2c):
    # initialize the sensor
    bus_write(i2c, TP_ADDR, TP_INIT)
    # send measurement command
    bus_write(i2c, TP_ADDR, TP_READ)
    # sleep for 1 second - this should be shorter (75ms according to the
    # datasheet), but on my board the sensor was returning a busy/reading
    # state (MSB of the first response byte)
    utime.sleep(1)
    # read data from the sensor, stop after 7 ack/nbytes. See datasheet for reference
    data = bus_read(i2c, TP_ADDR, 7)
    return data

def convert(i2c):
    data = read_values(i2c)
    # bt shifting of the binay data to rebuild the information
    bin_temp = ((data[3] & 0x0F) << 16) | (data[4] << 8) | data[5]
    bin_rh= ((data[1] << 16) | (data[2] << 8) | data[3]) >> 4
    # decimal conversion and rounding
    temp = round((((bin_temp / 1048576) * 200 ) - 50), PRECISION)
    rh   = round(((bin_rh / 1048576) * 100), PRECISION)
    return temp, rh

def detect_sensor(i2c):
    sensor=i2c.scan()
    if (int(sensor[0]) != 56):
        print("AHT10 sensors not detected, check cabling\nQuitting.")
        sys.exit(2)
    return 0

# setup the bus
i2c = machine.I2C(0, scl=machine.Pin(1), sda=machine.Pin(0), freq=400000)

# continuous reading
while True:
    detect_sensor(i2c)
    reading=convert(i2c)
    print('------------------------------------')
    print(f'Temperature: {reading[0]} °C')
    print(f'Relative Humidity: {reading[1]}%')
    print('')
    utime.sleep(2)

sys.exit(0)
