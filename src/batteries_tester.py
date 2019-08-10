
try:
    import RPi.GPIO as GPIO

    import board
except:
    pass


import busio
import digitalio

import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

import time
from datetime import datetime


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


def read_all_voltages_t(batt_infos, mcp):
    for batt_id in list(batt_infos.keys()):
        close_relay(batt_id, batt_infos)
        time.sleep(0.1)
        voltage = read_voltage(batt_id, batt_infos, mcp)
        open_relay(batt_id, batt_infos)
        print('Voltage batt ' + str(batt_id) + ": " + str(voltage) + 'V')


def set_up_conf():
    GPIO.setmode(GPIO.BCM)  # GPIO Numbers instead of board numbers

    # ==== MCP3008 hardware SPI configuration ====
    spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
    # create the cs (chip select)
    cs = digitalio.DigitalInOut(board.CE0)
    # create the mcp object (harware option)
    mcp = MCP.MCP3008(spi, cs)

    batt_infos = {
        1: {"relay_gpio": 5, "mcp_pin0": MCP.P0, "mcp_pin1": MCP.P1},
        2: {"relay_gpio": 6, "mcp_pin0": MCP.P2, "mcp_pin1": MCP.P3},
        3: {"relay_gpio": 13, "mcp_pin0": MCP.P4, "mcp_pin1": MCP.P5},
        4: {"relay_gpio": 19, "mcp_pin0": MCP.P6, "mcp_pin1": MCP.P7}
    }

    return mcp, batt_infos


class Battery:
    def __init__(self, tester_slot):
        self.tester_slot = tester_slot
        self.voltages_history = []


class BatteriesTester:

    def __init__(self):
        self.map_slots = {
            1: {"relay_gpio": 5, "mcp_pin0": MCP.P0, "mcp_pin1": MCP.P1},
            2: {"relay_gpio": 6, "mcp_pin0": MCP.P2, "mcp_pin1": MCP.P3},
            3: {"relay_gpio": 13, "mcp_pin0": MCP.P4, "mcp_pin1": MCP.P5},
            4: {"relay_gpio": 19, "mcp_pin0": MCP.P6, "mcp_pin1": MCP.P7}
        }

        GPIO.setmode(GPIO.BCM)  # GPIO Numbers instead of board numbers

        # ==== MCP3008 hardware SPI configuration ====
        spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
        # create the cs (chip select)
        cs = digitalio.DigitalInOut(board.CE0)
        # create the mcp object (harware option)
        self.mcp = MCP.MCP3008(spi, cs)

    def close_relay(self, battery):
        # ==== close the relay ====
        RELAY_GPIO = self.map_slots[battery.tester_slot]['relay_gpio']
        # GPIO Assign mode
        GPIO.setup(RELAY_GPIO, GPIO.OUT)
        # close the relay
        GPIO.output(RELAY_GPIO, GPIO.LOW)
        # we need some time between the actions of the different relays
        time.sleep(0.5)
        return

    def open_relay(self, battery):
        # ==== close the relay ====
        RELAY_GPIO = self.map_slots[battery.tester_slot]['relay_gpio']
        # GPIO Assign mode
        GPIO.setup(RELAY_GPIO, GPIO.OUT)
        # close the relay
        GPIO.output(RELAY_GPIO, GPIO.HIGH)
        # we need some time between the actions of the different relays
        time.sleep(0.5)
        return

    def read_voltage(self, battery):
        # create a differential ADC channel between Pin 0 and Pin 1
        pin0 = self.map_slots[battery.tester_slot]['mcp_pin0']
        pin1 = self.map_slots[battery.tester_slot]['mcp_pin0']
        voltage = AnalogIn(self.mcp, pin0, pin1).voltage
        battery.voltages_history.append([datetime.now(), voltage])

        return voltage


if __name__ == "__main__":
    nb_of_batteries = 4
    batteries = [Battery(x) for x in range(1, nb_of_batteries + 1)]

    batteries_tester = BatteriesTester()

    # close all the relays
    for battery in batteries:
        batteries_tester.close_relay(battery)














if __name__ == "__main__2":
    mcp, batt_infos = set_up_conf()

    # ==== beginning of the capacity measure ====

    # initialization of the measure:
    # close all the relays
    batt_measures = {}
    for batt_id in list(batt_infos.keys()):
        close_relay(batt_id, batt_infos)
        time.sleep(0.5)
        # initialize the dictionnary that records the measures
        batt_measures[batt_id] = {'voltages': [], 'capacity': 0}

    # read the voltages and record them
    i = 0
    while i < 3:
        for batt_id in list(batt_infos.keys()):
            voltage = read_voltage(batt_id, batt_infos, mcp)
            batt_measures[batt_id]['voltages'].append(voltage)
            print('batt ' + str(batt_id) + ": " + str(voltage))
        time.sleep(1)
        i += 1
    print(batt_measures)

    # for each battery
    # while the voltage > 3V, record the voltages
    # when voltage < 3V, open the relay of this battery, and send the total capacity

    # open all the relays
    for batt_id in list(batt_infos.keys()):
        open_relay(batt_id, batt_infos)
        time.sleep(0.5)