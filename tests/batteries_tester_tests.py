from src.batteries_tester import BatteriesTester, Battery, manage


import mock
import pytest
from pytest_mock import mocker
from mock import MagicMock, patch
from datetime import datetime


class BatteriesTesterMock:

    def close_relay(battery):
        self.history.append(
            {'time': datetime.now(), 'operation': 'close_relay', 'battery': battery.tester_slot, 'value': None})
        return

    def open_relay(battery):
        return

    def read_voltage(battery):
        print(t0)
        voltage = 2
        battery.voltages_history.append([datetime.now(), voltage])
        return 2


def test_tester():

    nb_of_batteries = 4
    batteries = [Battery(x) for x in range(1, nb_of_batteries + 1)]

    batteries_tester = BatteriesTester()


def test2():
    global t0
    t0 = datetime.now()

    nb_of_batteries = 4
    batteries = [Battery(x) for x in range(1, nb_of_batteries + 1)]

    batteries_tester = BatteriesTester()
    batteries_tester.close_relay = MagicMock(side_effect=BatteriesTesterMock.close_relay)
    batteries_tester.open_relay = MagicMock(side_effect=BatteriesTesterMock.open_relay)
    batteries_tester.read_voltage = MagicMock(side_effect=BatteriesTesterMock.read_voltage)

    manage(batteries_tester, batteries)
    a = 1