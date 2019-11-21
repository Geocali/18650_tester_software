
try:
    import RPi.GPIO as GPIO
    import board
    SIMULATION = False
except:

    SIMULATION = True


import busio
import digitalio

import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

import time
from datetime import datetime
import numpy as np


class Battery:
    def __init__(self, tester_slot):
        self.tester_slot = tester_slot
        self.voltages_history = []
        self.tested_capacity = None


class BatteriesTester:

    def __init__(self):
        self.map_slots = {
            1: {"relay_gpio": 5, "mcp_pin0": MCP.P0, "mcp_pin1": MCP.P1},
            2: {"relay_gpio": 6, "mcp_pin0": MCP.P2, "mcp_pin1": MCP.P3},
            3: {"relay_gpio": 13, "mcp_pin0": MCP.P4, "mcp_pin1": MCP.P5},
            4: {"relay_gpio": 19, "mcp_pin0": MCP.P6, "mcp_pin1": MCP.P7}
        }
        self.history = []
        self.setup()
        self.R = 4 # Ohm

    def setup(self):
        if not SIMULATION:
            GPIO.setmode(GPIO.BCM)  # GPIO Numbers instead of board numbers

            # ==== MCP3008 hardware SPI configuration ====
            spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
            # create the cs (chip select)
            cs = digitalio.DigitalInOut(board.CE0)
            # create the mcp object (harware option)
            self.mcp = MCP.MCP3008(spi, cs)
        else:
            pass

    def close_relay(self, battery):
        # ==== close the relay ====
        RELAY_GPIO = self.map_slots[battery.tester_slot]['relay_gpio']
        # GPIO Assign mode
        GPIO.setup(RELAY_GPIO, GPIO.OUT)
        # close the relay
        GPIO.output(RELAY_GPIO, GPIO.LOW)
        # we need some time between the actions of the different relays
        time.sleep(0.5)
        self.history.append({'time': datetime.now(), 'operation': 'close_relay', 'battery': battery.tester_slot, 'value': None})
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
        self.history.append({'time': datetime.now(), 'operation': 'open_relay', 'battery': battery.tester_slot, 'value': None})
        return

    def read_voltage(self, battery):
        # create a differential ADC channel between Pin 0 and Pin 1
        pin0 = self.map_slots[battery.tester_slot]['mcp_pin0']
        pin1 = self.map_slots[battery.tester_slot]['mcp_pin0']
        voltage = AnalogIn(self.mcp, pin0, pin1).voltage
        battery.voltages_history.append([datetime.now(), voltage])
        self.history.append({'time': datetime.now(), 'operation': 'read_voltage', 'battery': battery.tester_slot, 'value': voltage})
        return voltage


def manage(batteries_tester, batteries):

    # close all the relays
    for battery in batteries:
        batteries_tester.close_relay(battery)

    i = 0
    while i < 100:
        for battery in batteries:
            voltage = batteries_tester.read_voltage(battery)

            if voltage < 3:
                batteries_tester.open_relay(battery)
                battery.tested_capacity = sum(np.array(battery.voltages_history)[:,1]) / batteries_tester.R

        i += 1
    return


if __name__ == "__main__":
    nb_of_batteries = 4
    batteries = [Battery(x) for x in range(1, nb_of_batteries + 1)]

    batteries_tester = BatteriesTester()

    manage(batteries_tester, batteries)














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