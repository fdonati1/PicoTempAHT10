# PicoTempAHT10

## Temperature and relative humidity sensor
Built used a Raspberry Pi Pico W and the AHT10 sensor.

## AHT10
This seems to be a very common low-cost sensor, but with a decent precision.
I have compared the readings with other commercial sensors I have at home and the readins where very similar.

Unfortunately the documentation is quite poor, and certain datasheets are terrible (bad formatting, with some parts written in Chinese), so it was difficult to understand how to read the values, and I helped myself looking at some C library available in other repositories.

## Raspberry PI Pico W
The Raspberry Pi Pico W is a low-cost board with WiFi support which can be used with Micropython. All the ready-to-go libraries for the AHT10 I found around were using specific modules for the AHT10 or libraries like the smbus, which is not natively availabile in Micropython. Because I did not want to add any libray to the Pico, I wrote this simple module which is based on the I2C library. 
