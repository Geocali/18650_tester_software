i = 0

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

def AnalogIn(mcp, pin0, pin1):

    slot_id = pin0 / 2 + 1
    voltage_start = 0
    delta = 0.01
    if i == 0:
        # the program is starting
        if slot_id == 1:
            voltage_start = 0
        elif slot_id == 2:
            voltage_start = 0
        elif slot_id == 3:
            voltage_start = 0
        elif slot_id == 4:
            voltage_start = 0
    else:
        if slot_id == 1:
            voltage_start = 4.1 - delta * i
        elif slot_id == 2:
            voltage_start = 4.15 - delta * i
        elif slot_id == 3:
            voltage_start = 4.2 - delta * i
        elif slot_id == 4:
            voltage_start = 4.25 - delta * i

    # infos for this slot and last testing session
    class AnalogInclass:

        voltage = voltage_start * 3.3 / 5

    return AnalogInclass