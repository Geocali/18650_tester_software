from rpi_mock import *
import pytest

import json


def reset_state_file():
    with open("test_state.json","w") as f:
        jsons = json.dumps({1: 0, 2: 0, 3: 0, 4: 0})
        f.write(jsons)

def test_get_id_initial_index_is_zero():

    assert [get_i(1), get_i(2), get_i(3), get_i(4)] == [0, 0, 0, 0]


def test_get_id_increments_slot():
    
    slot_id = 1
    i1 = get_i(slot_id)
    i2 = get_i(slot_id)

    assert i2 == i1 + 1


def test_get_id_does_not_increment_other_slots():

    i_slot = [get_i(i) for i in range(1, 5)]
    i_slot1 = get_i(1)
    i_slot_updated = [get_i(i) for i in range(1, 5)]

    assert (i_slot_updated[1:] == [x + 1 for x in i_slot[1:]]) and (i_slot_updated[0] == (i_slot[0] + 2))


def test_voltage_reading_first_value():

    cs = digitalio.DigitalInOut(board.CE0)
    spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
    mcp = MCP.MCP3008(spi, cs)

    reset_state_file()

    pin0 = 0
    pin1 = None
    voltage = AnalogIn(mcp, pin0, pin1).voltage / 3.3 * 5
    assert voltage == 0

def test_voltage_readings():

    cs = digitalio.DigitalInOut(board.CE0)
    spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
    mcp = MCP.MCP3008(spi, cs)

    reset_state_file()

    pin0 = 0
    pin1 = None
    voltage1 = AnalogIn(mcp, pin0, pin1).voltage / 3.3 * 5
    voltage2 = AnalogIn(mcp, pin0, pin1).voltage / 3.3 * 5
    voltage3 = AnalogIn(mcp, pin0, pin1).voltage / 3.3 * 5

    assert voltage1 == 0
    assert voltage3 < voltage2


if __name__ == "__main__":
    test_voltage_readings()

    a = 1