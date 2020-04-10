import tester
import pytest
import json
import dill
import os
import numpy as np


class TestClass():
    def setup_method(self):
        with open("test_state.json","w") as f:
            jsons = json.dumps({1: 0, 2: 0, 3: 0, 4: 0})
            f.write(jsons)

        csv_file = 'output/measures.csv'
        if os.path.exists(csv_file):
            os.remove(csv_file)

    def teardown_class(self):
        print("teardown_class called once for the class")


    def test_when_a_charged_battery_is_present_the_test_is_started(self):
        
        # ---- define voltage reading mock function and export it ----
        def read_voltage(slot_id, i):
            vmax = 4.2
            delta = 0.1
            if i == 0:
                voltage_measured = 0
            else:
                if slot_id == 1:
                    voltage_measured = vmax - delta * i
                    if voltage_measured < 3:
                        voltage_measured = 3
                else:
                    voltage_measured = 0
            return voltage_measured
        with open('read_voltage.pkl', 'wb') as file:
            dill.dump(read_voltage, file)
        
        # launch the voltage reading once
        df_slots_history = tester.main_function()

        # there shall be 1 reading for each slot 
        assert np.array_equal(df_slots_history.slot_id.values, [1, 2, 3, 4])
        # the testing shall be ongoing only for the slot 1
        assert np.array_equal(df_slots_history.testing.values, [1, 0, 0, 0])


if __name__ == "__main__":
    tests = TestClass()
    tests.setup_method()
    tests.test_when_a_charged_battery_is_present_the_measures_are_correct()
