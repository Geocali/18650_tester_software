import tkinter_app
import tkinter
import pytest
import dill
# import threading
import numpy as np
import os
import json
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

        # Creation of empty plot
        self.tester_gui = tkinter_app.TesterOutline(True)

    def teardown_method(self):
        self.tester_gui.quit()

    def test_a_charged_battery_is_inserted_the_test_is_starting(self):
        def read_voltage(slot_id, i):
            vmax = 4.2
            
            if i < 2:
                voltage_measured = 0
            elif i >= 2 and i < 15:
                delta = 0.1
                if slot_id == 1:
                    voltage_measured = vmax - delta * (i - 2)
                    if voltage_measured < 2.8:
                        voltage_measured = 2.8
                else:
                    voltage_measured = 0
            else:
                # replacement of the battery
                voltage_measured = 0
            return voltage_measured
        with open('read_voltage.pkl', 'wb') as file:
            dill.dump(read_voltage, file)

        assert np.array_equal(self.tester_gui.axes[0].lines[0]._path.vertices, [[0, 0]])
        # first measure, without battery
        self.tester_gui.update_plot(self.tester_gui.graph)
        assert len(self.tester_gui.axes[0].texts) == 1
        assert self.tester_gui.axes[0].texts[0]._text == "Waiting for battery"
        # second measure, with battery
        self.tester_gui.update_plot(self.tester_gui.graph)
        assert len(self.tester_gui.axes[0].texts) == 1
        assert self.tester_gui.axes[0].texts[0]._text == "A charged battery is \ninserted, starting test"
        assert len(self.tester_gui.axes[0].lines[0]._path.vertices) == 1
        assert self.tester_gui.axes[0].lines[0]._path.vertices[0][1]== 4.2
        # third measure, with battery
        self.tester_gui.update_plot(self.tester_gui.graph)
        assert np.array_equal(self.tester_gui.axes[0].lines[0]._path.vertices[:,1], [4.2, 4.1])


    def test_a_discharged_battery_is_inserted_the_test_is_not_starting(self):
        def read_voltage(slot_id, i):
            vmax = 3.8
            if i < 2:
                voltage_measured = 0
            else:
                delta = 0.1
                if slot_id == 1:
                    voltage_measured = vmax - delta * (i - 2)
                else:
                    voltage_measured = 0
            return voltage_measured
        with open('read_voltage.pkl', 'wb') as file:
            dill.dump(read_voltage, file)

        # first measure, without battery
        self.tester_gui.update_plot(self.tester_gui.graph)
        assert len(self.tester_gui.axes[0].texts) == 1
        assert self.tester_gui.axes[0].texts[0]._text == "Waiting for battery"
        # second measure, with battery
        self.tester_gui.update_plot(self.tester_gui.graph)
        assert len(self.tester_gui.axes[0].texts) == 1
        assert self.tester_gui.axes[0].texts[0]._text == "The inserted battery is \nnot fully charged \ntest not starting"
        self.tester_gui.update_plot(self.tester_gui.graph)
        assert self.tester_gui.axes[0].texts[0]._text == "The inserted battery is \nnot fully charged \ntest not starting"

    
    def test_a_battery_is_removed_before_end_of_test(self):
        def read_voltage(slot_id, i):
            vmax = 4.2
            if i < 2:
                voltage_measured = 0
            elif i >= 2 and i < 8:
                delta = 0.1
                if slot_id == 1:
                    voltage_measured = vmax - delta * (i - 2)
                else:
                    voltage_measured = 0
            else:
                voltage_measured = 0
            return voltage_measured
        with open('read_voltage.pkl', 'wb') as file:
            dill.dump(read_voltage, file)

        # first measure, without battery
        self.tester_gui.update_plot(self.tester_gui.graph)
        assert len(self.tester_gui.axes[0].texts) == 1
        assert self.tester_gui.axes[0].texts[0]._text == "Waiting for battery"
        # second measure, with battery
        self.tester_gui.update_plot(self.tester_gui.graph)
        assert len(self.tester_gui.axes[0].texts) == 1
        assert self.tester_gui.axes[0].texts[0]._text == "A charged battery is \ninserted, starting test"
        self.tester_gui.update_plot(self.tester_gui.graph)
        self.tester_gui.update_plot(self.tester_gui.graph)
        self.tester_gui.update_plot(self.tester_gui.graph)
        self.tester_gui.update_plot(self.tester_gui.graph)
        self.tester_gui.update_plot(self.tester_gui.graph)
        self.tester_gui.update_plot(self.tester_gui.graph)
        assert self.tester_gui.axes[0].texts[0]._text == "Test interrupted \nWaiting for battery"

    
    def test_a_charged_battery_is_inserted_after_interrupted_test(self):
        def read_voltage(slot_id, i):
            vmax = 4.2
            delta = 0.1
            if i < 2:
                voltage_measured = 0
            elif i >= 2 and i < 8:
                if slot_id == 1:
                    voltage_measured = vmax - delta * (i - 2)
                else:
                    voltage_measured = 0
            elif (i >= 10) and (slot_id == 1):
                voltage_measured = vmax - delta * (i - 10)
            else:
                voltage_measured = 0
            return voltage_measured
        with open('read_voltage.pkl', 'wb') as file:
            dill.dump(read_voltage, file)

        # first measure, without battery
        self.tester_gui.update_plot(self.tester_gui.graph)
        self.tester_gui.update_plot(self.tester_gui.graph)
        self.tester_gui.update_plot(self.tester_gui.graph)
        self.tester_gui.update_plot(self.tester_gui.graph)
        self.tester_gui.update_plot(self.tester_gui.graph)
        self.tester_gui.update_plot(self.tester_gui.graph)
        self.tester_gui.update_plot(self.tester_gui.graph)
        self.tester_gui.update_plot(self.tester_gui.graph)
        self.tester_gui.update_plot(self.tester_gui.graph)
        self.tester_gui.update_plot(self.tester_gui.graph)
        assert self.tester_gui.axes[0].texts[0]._text == "A charged battery is \ninserted, starting test"

    def test_an_empty_battery_is_inserted_after_interrupted_test(self):
        def read_voltage(slot_id, i):
            vmax = 4.2
            delta = 0.1
            if i < 2:
                voltage_measured = 0
            elif i >= 2 and i < 8:
                if slot_id == 1:
                    voltage_measured = vmax - delta * (i - 2)
                else:
                    voltage_measured = 0
            elif (i >= 10) and (slot_id == 1):
                voltage_measured = 3.5 - delta * (i - 10)
            else:
                voltage_measured = 0
            return voltage_measured
        with open('read_voltage.pkl', 'wb') as file:
            dill.dump(read_voltage, file)

        # first measure, without battery
        self.tester_gui.update_plot(self.tester_gui.graph)
        self.tester_gui.update_plot(self.tester_gui.graph)
        self.tester_gui.update_plot(self.tester_gui.graph)
        self.tester_gui.update_plot(self.tester_gui.graph)
        self.tester_gui.update_plot(self.tester_gui.graph)
        self.tester_gui.update_plot(self.tester_gui.graph)
        self.tester_gui.update_plot(self.tester_gui.graph)
        self.tester_gui.update_plot(self.tester_gui.graph)
        self.tester_gui.update_plot(self.tester_gui.graph)
        self.tester_gui.update_plot(self.tester_gui.graph)
        assert self.tester_gui.axes[0].texts[0]._text == "The inserted battery is \nnot fully charged \ntest not starting"


    def test_a_battery_test_is_completed(self):
        def read_voltage(slot_id, i):
            vmax = 4.2
            if i < 2:
                voltage_measured = 0
            else:
                delta = 0.5
                if slot_id == 1:
                    voltage_measured = vmax - delta * (i - 2)
                else:
                    voltage_measured = 0
            return voltage_measured
        with open('read_voltage.pkl', 'wb') as file:
            dill.dump(read_voltage, file)

        # first measure, without battery
        self.tester_gui.update_plot(self.tester_gui.graph)
        self.tester_gui.update_plot(self.tester_gui.graph)
        self.tester_gui.update_plot(self.tester_gui.graph)
        self.tester_gui.update_plot(self.tester_gui.graph)
        self.tester_gui.update_plot(self.tester_gui.graph)
        assert "The test is completed!" in self.tester_gui.axes[0].texts[0]._text

    def test_a_test_is_completed_another_test_begins(self):
        def read_voltage(slot_id, i):
            vmax = 4.2
            if i < 2:
                voltage_measured = 0
            else:
                delta = 0.1
                if slot_id == 1:
                    voltage_measured = vmax - delta * (i - 2)
                else:
                    voltage_measured = 0
            return voltage_measured
        with open('read_voltage.pkl', 'wb') as file:
            dill.dump(read_voltage, file)

        # first measure, without battery
        for i in range(50):
            self.tester_gui.update_plot(self.tester_gui.graph)

        # assert "The test is completed!" in self.tester_gui.axes[0].texts[0]._text



if __name__ == "__main__":
    tests = TestClass()
    tests.test_a_charged_battery_is_inserted_the_test_is_starting()