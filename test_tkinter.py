import tkinter_app
import pytest
import dill

class TestClass():

    def test_1(self):
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


        tester_gui = tkinter_app.TesterOutline()
        tester_gui.mainloop()

if __name__ == "__main__":
    tests = TestClass()
    tests.test_1()