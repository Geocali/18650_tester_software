import json
import dill


class MCP:
    P0 = 0
    P1 = 1
    P2 = 2
    P3 = 3
    P4 = 4
    P5 = 5
    P6 = 6
    P7 = 7

    def MCP3008(spi, cs):
        return None

class board:
    SCK = "SCK"
    MISO = "MISO"
    MOSI = "MOSI"
    CE0 = "CE0"

class busio:
    def SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI):
        return None

class digitalio:
    def DigitalInOut(CE0):
        return None

class GPIO:
    OUT = "OUT"
    HIGH = "HIGH"
    LOW = "LOW"

    def setup(a, b):
        return None

    def output(selfa, b):
        return None


with open("test_state.json","w") as f:
    jsons = json.dumps({1: 0, 2: 0, 3: 0, 4: 0})
    f.write(jsons)


def get_i(slot_id):
    slot_id = str(int(float(slot_id)))
    with open('test_state.json') as json_file: 
        test_state = json.load(json_file)
    i = test_state[slot_id]
    test_state[slot_id] += 1
    jsons = json.dumps(test_state)
    with open("test_state.json","w") as f:
        f.write(jsons)
    return i


def AnalogIn(mcp, pin0, pin1):
    slot_id = pin0 / 2 + 1
    # TODO: remove usage of test_state.json, and count the recordings in output/measures.csv
    i = get_i(slot_id)

    # ---- read mock function in file ----
    # read_voltage = dill.load("read_voltage.pkl")
    with open("read_voltage.pkl", 'rb') as pickle_file:
        read_voltage = dill.load(pickle_file)


    voltage_measured = read_voltage(i)

    # vmax = 4.2
    # delta = 0.1
    # if i == 0:
    #     voltage_measured = 0
    # else:
    #     voltage_measured = vmax - delta * i
    #     if voltage_measured < 3:
    #         voltage_measured = 3

    # infos for this slot and last testing session
    class AnalogInclass:
        voltage = voltage_measured * 3.3 / 5

    return AnalogInclass