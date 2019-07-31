import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers

import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

import time


def close_relay(batt_id, batt_infos):
    # ==== close the relay ====
    RELAY_GPIO = batt_infos[batt_id]["relay_gpio"]
    # GPIO Assign mode
    GPIO.setup(RELAY_GPIO, GPIO.OUT)
    # close the relay
    GPIO.output(RELAY_GPIO, GPIO.LOW)
    return

def open_relay(batt_id, batt_infos):
    # ==== close the relay ====
    RELAY_GPIO = batt_infos[batt_id]["relay_gpio"]
    # GPIO Assign mode
    GPIO.setup(RELAY_GPIO, GPIO.OUT)
    # close the relay
    GPIO.output(RELAY_GPIO, GPIO.HIGH)
    return

def read_voltage(batt_id, batt_infos, mcp):
    # create a differential ADC channel between Pin 0 and Pin 1
    pin0 = batt_infos[batt_id]["mcp_pin0"]
    pin1 = batt_infos[batt_id]["mcp_pin1"]
    return AnalogIn(mcp, pin0, pin1).voltage

batt_infos = {
    1: {"relay_gpio":5, "mcp_pin0": MCP.P0, "mcp_pin1": MCP.P1},
    2: {"relay_gpio":6, "mcp_pin0": MCP.P2, "mcp_pin1": MCP.P3},
    3: {"relay_gpio":13, "mcp_pin0": MCP.P4, "mcp_pin1": MCP.P5},
    4: {"relay_gpio":19, "mcp_pin0": MCP.P6, "mcp_pin1": MCP.P7}
}

# ==== measure the voltage ====

# MCP3008 hardware SPI configuration
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
# create the cs (chip select)
cs = digitalio.DigitalInOut(board.CE0)
# create the mcp object (harware option)
mcp = MCP.MCP3008(spi, cs)

for batt_id in list(batt_infos.keys()):
    close_relay(batt_id, batt_infos)
    time.sleep(0.1)
    voltage = read_voltage(batt_id, batt_infos, mcp)
    open_relay(batt_id, batt_infos)
    print('Voltage batt ' + str(batt_id) + ": " + str(voltage) + 'V')

