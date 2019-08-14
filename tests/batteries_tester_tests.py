from src.batteries_tester import BatteriesTester, Battery, manage


import mock
import pytest
from pytest_mock import mocker
from mock import MagicMock, patch
from datetime import datetime


class BatteriesTesterMockCase1:
    def __init__(self):
        self.history = []
        self.R = 4 # Ohm
        self.relays = {1: 'open', 2: 'open', 3: 'open', 4: 'open'}

        return

    def close_relay(self, battery):
        self.history.append({
            'time': datetime.now(),
            'operation': 'close_relay',
            'battery': battery.tester_slot,
            'value': None})
        self.relays[battery.tester_slot] = 'closed'
        return

    def open_relay(self, battery):
        self.history.append({
            'time': datetime.now(),
            'operation': 'open_relay',
            'battery': battery.tester_slot,
            'value': None})
        self.relays[battery.tester_slot] = 'open'
        return

    def read_voltage(self, battery):
        # at each voltage reading of a battery, the voltage decreases
        if len(battery.voltages_history) == 0:
            if self.relays[battery.tester_slot] == 'closed':
                # when we close the relay, the voltage decreases because of the load
                voltage = 4
            else:
                # when the relay is open, there is no current in the resistor
                voltage = 0
        else:
            if self.relays[battery.tester_slot] == 'closed':
                # if the relay has never been open during the test
                voltage = 4
                # if the relay has been open during the test, we add a voltage
            else:
                # when the relay is open, there is no current in the resistor
                voltage = 0

        voltage = 4 - 0.1 * len(battery.voltages_history)

        self.history.append({
            'time': datetime.now(),
            'operation': 'read_voltage',
            'battery': battery.tester_slot,
            'value': voltage})
        battery.voltages_history.append([datetime.now(), voltage])
        return voltage


class BatteriesTesterMockCase2(BatteriesTesterMockCase1):

    def read_voltage(self, battery):
        # at each voltage reading of a battery, the voltage decreases if the relay is closed
        voltage = 3 - 0.1 * len(battery.voltages_history)

        self.history.append({
            'time': datetime.now(),
            'operation': 'read_voltage',
            'battery': battery.tester_slot,
            'value': voltage})
        battery.voltages_history.append([datetime.now(), voltage])
        return voltage


def test_tester():

    nb_of_batteries = 4
    batteries = [Battery(x) for x in range(1, nb_of_batteries + 1)]

    batteries_tester = BatteriesTester()


def test_case1():
    # case 1:
    # - put battery charged. The voltage passes from 4.2V to a little less (4V)
    # - the battery is discharged, the relay opens. The voltage raises a little above 3V

    nb_of_batteries = 4
    batteries = [Battery(x) for x in range(1, nb_of_batteries + 1)]

    batteries_tester = BatteriesTesterMockCase1()

    manage(batteries_tester, batteries)
    a = 1
    #assert batteries[0].tested_capacity ==

