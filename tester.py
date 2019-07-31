import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers

import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

# ==== close the relay ====
RELAIS_1_GPIO = 6
# GPIO Assign mode
GPIO.setup(RELAIS_1_GPIO, GPIO.OUT)
# close the relay
GPIO.output(RELAIS_1_GPIO, GPIO.LOW)

# ==== measure the voltage ====
# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D5)

# create the mcp object
mcp = MCP.MCP3008(spi, cs)

# create a differential ADC channel between Pin 0 and Pin 1
chan = AnalogIn(mcp, MCP.P0, MCP.P1)

print('Differential ADC Value: ', chan.value)
print('Differential ADC Voltage: ' + str(chan.voltage) + 'V')



# ==== open the relay ====
#GPIO.output(RELAIS_1_GPIO, GPIO.HIGH) # open the relay