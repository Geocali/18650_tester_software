from battery_tester import tester
import pytest
import json
import dill
import os
import numpy as np
import re


class TestClass():
    def setup_class(self):
        if not os.path.exists("output"):
            os.mkdir("output")
            self.existant_csv = []
        else:
            self.existant_csv = [f for f in os.listdir('output') if re.match(r'[0-9]{4}.*mAh\.csv', f)]

    def teardown_class(self):
        new_csv = [f for f in os.listdir('output') if re.match(r'[0-9]{4}.*mAh\.csv', f)]
        created_csv = np.setdiff1d(new_csv, self.existant_csv)
        for csv in created_csv:
            os.remove("output/" + csv)

    def setup_method(self):
        with open("test_state.json","w") as f:
            jsons = json.dumps({1: 0, 2: 0, 3: 0, 4: 0})
            f.write(jsons)

        csv_file = 'output/measures.csv'
        if os.path.exists(csv_file):
            os.remove(csv_file)


    def test_when_a_charged_battery_is_present_the_test_is_started(self):
        
        # ---- define voltage reading mock function and export it ----
        def read_voltage(slot_id, i):
            vmax = 4.2
            delta = 0.1
            if i < 2:
                voltage_measured = 0
            else:
                if slot_id == 1:
                    voltage_measured = vmax - delta * (i - 2)
                    if voltage_measured < 3:
                        voltage_measured = 3
                else:
                    voltage_measured = 0
            return voltage_measured
        with open('read_voltage.pkl', 'wb') as file:
            dill.dump(read_voltage, file)
        
        # launch the voltage reading for i = 0
        df_slots_history = tester.main_function()
        # launch the voltage reading for i = 1
        df_slots_history = tester.main_function()

        # there shall be 2 readings for each slot 
        assert np.array_equal(df_slots_history.slot_id.values, [1, 2, 3, 4, 1, 2, 3, 4])
        # the testing shall be ongoing only for the slot 1 at the time of the second measure
        assert np.array_equal(df_slots_history.testing.values, [0, 0, 0, 0, 1, 0, 0, 0])
        # the first voltage of the battery during the test shall be 4.2
        assert np.array_equal(df_slots_history.voltage.values, [0, 0, 0, 0, 4.2, 0, 0, 0])
        # the calculated capacity in mAh shall be around 1s x 4.2V / 4Ohm / 3600s * 1000 = 0,2916
        assert pytest.approx(0,2916, 0.01)

    def test_when_a_battery_under_test_passes_under_3V_the_test_is_stopped_and_a_report_is_created(self):
        
        # ---- define voltage reading mock function and export it ----
        def read_voltage(slot_id, i):
            vmax = 4.2
            delta = 0.5
            if i < 2:
                voltage_measured = 0
            else:
                if slot_id == 1:
                    voltage_measured = vmax - delta * (i - 2)
                    if voltage_measured < 2.8:
                        voltage_measured = 2.8
                else:
                    voltage_measured = 0
            return voltage_measured
        with open('read_voltage.pkl', 'wb') as file:
            dill.dump(read_voltage, file)

        # list existing csv report files
        reports0 = [f for f in os.listdir('output') if re.match(r'[0-9]{4}.*mAh\.csv', f)]
        
        for i in range(5):
            df_slots_history = tester.main_function()
        reports1 = [f for f in os.listdir('output') if re.match(r'[0-9]{4}.*mAh\.csv', f)]
        created_reports = np.setdiff1d(reports1, reports0)

        # the testing shall start when we insert the charged battery, and stop when it reaches 3V
        mask_3V = df_slots_history[df_slots_history.slot_id==1].voltage.values > 3
        assert np.array_equal(mask_3V, df_slots_history[df_slots_history.slot_id==1].testing.values)
        assert len(created_reports) == 1
        assert "_1_1_0mAh.csv" in created_reports[0]


    def test_when_we_remove_battery_before_end_of_test_no_csv_report_is_created(self):
        # ---- define voltage reading mock function and export it ----
        def read_voltage(slot_id, i):
            vmax = 4.2
            delta = 0.5
            if i < 2:
                voltage_measured = 0
            if i > 4:
                voltage_measured = 0
            else:
                if slot_id == 1:
                    voltage_measured = vmax - delta * (i - 2)
                    if voltage_measured < 2.8:
                        voltage_measured = 2.8
                else:
                    voltage_measured = 0
            return voltage_measured
        with open('read_voltage.pkl', 'wb') as file:
            dill.dump(read_voltage, file)

        # list existing csv report files
        reports0 = [f for f in os.listdir('output') if re.match(r'[0-9]{4}.*mAh\.csv', f)]
        
        for i in range(5):
            tester.main_function()
        reports1 = [f for f in os.listdir('output') if re.match(r'[0-9]{4}.*mAh\.csv', f)]
        created_reports = np.setdiff1d(reports1, reports0)

        # the testing won't finish, so no report shall be created
        assert len(created_reports) == 0

    def test_testing_of_a_battery_is_finished_voltage_rises_but_no_new_test_is_started(self):
        # ---- define voltage reading mock function and export it ----
        def read_voltage(slot_id, i):
            vmax = 4.2
            delta = 0.5
            if i < 2:
                voltage_measured = 0
            elif i >= 2 and i < 6:
                if slot_id == 1:
                    voltage_measured = vmax - delta * (i - 2)
                    if voltage_measured < 2.8:
                        voltage_measured = 2.8
                else:
                    voltage_measured = 0
            else:
                if slot_id == 1:
                    voltage_measured = vmax - delta * (i - 6)
                    if voltage_measured < 2.8:
                        voltage_measured = 2.8
                else:
                    voltage_measured = 0
            return voltage_measured
        with open('read_voltage.pkl', 'wb') as file:
            dill.dump(read_voltage, file)

        # list existing csv report files
        reports0 = [f for f in os.listdir('output') if re.match(r'[0-9]{4}.*mAh\.csv', f)]
        
        for i in range(10):
            tester.main_function()

        reports1 = [f for f in os.listdir('output') if re.match(r'[0-9]{4}.*mAh\.csv', f)]
        created_reports = np.setdiff1d(reports1, reports0)
        assert len(created_reports) == 1


    def test_testing_of_a_battery_is_finished_after_replacement_a_new_test_starts(self):
        # ---- define voltage reading mock function and export it ----
        def read_voltage(slot_id, i):
            vmax = 4.2
            delta = 0.5
            if i < 2:
                voltage_measured = 0
            elif i >= 2 and i < 6:
                if slot_id == 1:
                    voltage_measured = vmax - delta * (i - 2)
                    if voltage_measured < 2.8:
                        voltage_measured = 2.8
                else:
                    voltage_measured = 0
            elif i == 6:
                # replacement of the battery
                voltage_measured = 0
            else:
                if slot_id == 1:
                    voltage_measured = vmax - delta * (i - 7)
                    if voltage_measured < 2.8:
                        voltage_measured = 2.8
                else:
                    voltage_measured = 0
            return voltage_measured
        with open('read_voltage.pkl', 'wb') as file:
            dill.dump(read_voltage, file)

        # list existing csv report files
        reports0 = [f for f in os.listdir('output') if re.match(r'[0-9]{4}.*mAh\.csv', f)]
        
        for i in range(10):
            tester.main_function()

        reports1 = [f for f in os.listdir('output') if re.match(r'[0-9]{4}.*mAh\.csv', f)]
        created_reports = np.setdiff1d(reports1, reports0)
        assert len(created_reports) == 2


    def test_testing_of_a_battery_is_interrupted_after_replacement_a_new_test_starts(self):
        # ---- define voltage reading mock function and export it ----
        def read_voltage(slot_id, i):
            vmax = 4.2
            
            if i < 2:
                voltage_measured = 0
            elif i >= 2 and i < 6:
                delta = 0.1
                if slot_id == 1:
                    voltage_measured = vmax - delta * (i - 2)
                    if voltage_measured < 2.8:
                        voltage_measured = 2.8
                else:
                    voltage_measured = 0
            elif i == 6:
                # replacement of the battery
                voltage_measured = 0
            else:
                delta = 0.5
                if slot_id == 1:
                    voltage_measured = vmax - delta * (i - 7)
                    if voltage_measured < 2.8:
                        voltage_measured = 2.8
                else:
                    voltage_measured = 0
            return voltage_measured
        with open('read_voltage.pkl', 'wb') as file:
            dill.dump(read_voltage, file)

        # list existing csv report files
        reports0 = [f for f in os.listdir('output') if re.match(r'[0-9]{4}.*mAh\.csv', f)]
        
        for i in range(10):
            tester.main_function()

        reports1 = [f for f in os.listdir('output') if re.match(r'[0-9]{4}.*mAh\.csv', f)]
        created_reports = np.setdiff1d(reports1, reports0)
        assert len(created_reports) == 1


if __name__ == "__main__":
    tests = TestClass()
    tests.setup_method()
    tests.test_testing_of_a_battery_is_interrupted_after_replacement_a_new_test_starts()
