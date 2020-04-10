import tester
import pytest
import json
import dill

def atest():
    # ---- set initial state ----
    test_state = {1: 0, 2: 0, 3: 0, 4: 0}
    jsons = json.dumps(test_state)
    f = open("test_state.json","w")
    f.write(jsons)
    f.close()

    # ---- define voltage reading mock function and export it ----
    def read_voltage(i):
        vmax = 4.2
        delta = 0.1
        if i == 0:
            voltage_measured = 0
        else:
            voltage_measured = vmax - delta * i
            if voltage_measured < 3:
                voltage_measured = 3
        return voltage_measured
    with open('read_voltage.pkl', 'wb') as file:
        dill.dump(read_voltage, file)
    
    tester.main_function()


if __name__ == "__main__":
    atest()
