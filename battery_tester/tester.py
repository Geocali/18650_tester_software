import pandas as pd
import time
from datetime import datetime
import sys
import os.path


try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers
    import busio
    import digitalio
    import board
    import adafruit_mcp3xxx.mcp3008 as MCP
    from adafruit_mcp3xxx.analog_in import AnalogIn
except:
    # we are not on a raspberry, but we still can do some tests
    from battery_tester.rpi_mock import *


# ==== global parameters ====
# voltage under which we consider the battery as discharged
discharged_voltage = 3
# voltage above which we consider the battery as new
min_charged_voltage = 4
# value of the resistor
R = 4 # Ohm
# maximum voltage that we can read when there is no battery in the slot
voltage_empty_slot = 1


def close_relay(slot_id, slot_infos):
    # ==== close the relay ====
    RELAY_GPIO = slot_infos[slot_id]["relay_gpio"]
    # GPIO Assign mode
    GPIO.setup(RELAY_GPIO, GPIO.OUT)
    # close the relay
    GPIO.output(RELAY_GPIO, GPIO.LOW)
    slot_infos[slot_id]["relay_open"] = False
    time.sleep(0.5)
    return


def open_relay(slot_id, slot_infos):
    # ==== close the relay ====
    RELAY_GPIO = slot_infos[slot_id]["relay_gpio"]
    # GPIO Assign mode
    GPIO.setup(RELAY_GPIO, GPIO.OUT)
    # close the relay
    GPIO.output(RELAY_GPIO, GPIO.HIGH)
    slot_infos[slot_id]["relay_open"] = True
    time.sleep(0.5)
    return


def read_voltage(slot_id, slot_infos, mcp):
    # create a differential ADC channel between Pin 0 and Pin 1
    pin0 = slot_infos[slot_id]["mcp_pin0"]
    pin1 = slot_infos[slot_id]["mcp_pin1"]
    time.sleep(0.1)
    voltage = AnalogIn(mcp, pin0, pin1).voltage / 3.3 * 5
    return voltage


def read_all_voltages_t(slot_infos, mcp):
    for slot_id in list(slot_infos.keys()):
        close_relay(slot_id, slot_infos)
        time.sleep(0.1)
        voltage = read_voltage(slot_id, slot_infos, mcp)
        open_relay(slot_id, slot_infos)
        print('Voltage batt ' + str(slot_id) + ": " + str(voltage) + 'V')


def relays_initialization(slot_infos, mcp, csv_file):
    mah = 0
    # close all the relays of the slots containing a charged battery
    df_slots_history = pd.DataFrame()
    for slot_id in list(slot_infos.keys()):
        open_relay(slot_id, slot_infos)
        voltage = read_voltage(slot_id, slot_infos, mcp)

        # we record it
        if os.path.isfile(csv_file):
            df = pd.read_csv(csv_file)
            if df[df.slot_id == slot_id].shape[0] > 0:
                testing_session = int(df[df.slot_id == slot_id].testing_session.values[-1])
            else:
                testing_session = 0
        else:
            testing_session = 0
        slot_measure = pd.Series(
            data=[datetime.now(), slot_id, voltage, False, testing_session, mah],
            index=['time', 'slot_id', 'voltage', 'testing', 'testing_session', 'spent_mah']
        )
        df_slots_history = df_slots_history.append(slot_measure, ignore_index=True)

        # if the battery is charged, we test it
        if voltage > min_charged_voltage:
            close_relay(slot_id, slot_infos)

            # we record it (we read the voltage again, in case the relay is closed)
            voltage = read_voltage(slot_id, slot_infos, mcp)
            
            slot_measure = pd.Series(
                data=[datetime.now(), slot_id, voltage, True, testing_session, mah],
                index=['time', 'slot_id', 'voltage', 'testing', 'testing_session', 'spent_mah']
            )

            df = pd.DataFrame(slot_measure)
            df[0] = df[0].astype(str)
            if os.path.isfile(csv_file):
                df.T.to_csv(csv_file, mode='a', header=False, index=False)
            else:
                df.T.to_csv(csv_file, index=False)

            df_slots_history = df_slots_history.append(slot_measure, ignore_index=True)
    return df_slots_history


def main_function(csv_file='output/measures.csv'):
    slot_infos = {
        1: {"relay_gpio":5, "mcp_pin0": MCP.P0, "mcp_pin1": MCP.P1, "relay_open": True, "testing": False},
        2: {"relay_gpio":6, "mcp_pin0": MCP.P2, "mcp_pin1": MCP.P3, "relay_open": True, "testing": False},
        3: {"relay_gpio":13, "mcp_pin0": MCP.P4, "mcp_pin1": MCP.P5, "relay_open": True, "testing": False},
        4: {"relay_gpio":19, "mcp_pin0": MCP.P6, "mcp_pin1": MCP.P7, "relay_open": True, "testing": False}
    }

    # ==== MCP3008 hardware SPI configuration ====
    spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
    # create the cs (chip select)
    cs = digitalio.DigitalInOut(board.CE0)
    # create the mcp object (harware option)
    mcp = MCP.MCP3008(spi, cs)

    # ==== beginning of the capacity measure ====
    # we initialize the relays only at the beginning
    if not os.path.exists(csv_file):
        df_slots_history = relays_initialization(slot_infos, mcp, csv_file)
        first_measure = True
    else:
        df_slots_history = pd.read_csv(csv_file)
        first_measure = False
        
    # print('===========')
    for slot_id in list(slot_infos.keys()):
        
        # we read the voltage of the battery
        voltage = read_voltage(slot_id, slot_infos, mcp)

        last_measure = df_slots_history[df_slots_history.slot_id == slot_id].tail(1)
        last_testing_session = last_measure.testing_session.values[0]
        last_testing = bool(last_measure.testing.values[0])
        last_voltage = float(last_measure.voltage.values[0])
        last_mah = float(last_measure.spent_mah.values[0])
        mah = 0

        # ============= Case 1 ==================
        # - the preceding voltage was > discharged_voltage
        # - and current voltage < discharged_voltage
        # - and the battery is under testing
        # we send the conclusions and open the relay
        # print("-----", last_voltage, voltage, last_testing)

        if (
            (last_voltage > discharged_voltage)
            and (voltage <= discharged_voltage)
            and (voltage > voltage_empty_slot)
            and last_testing == True
        ):
            print("case 1, end of battery testing")
            
            # we calculate the total capacity
            df_testing_session = df_slots_history[
                (df_slots_history.slot_id == slot_id)
                & (df_slots_history.testing_session == last_testing_session)
                & (df_slots_history.testing == True)
            ]
            battery_capacity = df_testing_session.spent_mah.max()
            print('battery ' + str(slot_id) + ' tested at ' + str(round(battery_capacity, 0)) + ' mAh')
            
            # export to file
            filename = str(datetime.now())[0:19].replace(":", "") + "_" + str(slot_id) + "_" + str(int(last_testing_session)) + "_" + str(int(battery_capacity)) + "mAh.csv"
            df_testing_session.to_csv("output/" + filename, sep=",", index=False)
            
            open_relay(slot_id, slot_infos)
            last_testing = False

        # ============= Case 3 ============= 
        # if
        # - the preceding voltage was > 0(+delta)
        # - and now we have 0(+delta)
        # this means that the battery was removed from the slot
        # - the battery was under testing: don't send any conclusion about the capacity, reset
        # - the battery was already tested: reset
        
        if (
            (last_voltage > voltage_empty_slot)
            and (voltage < voltage_empty_slot)
        ):
            # print("case 3, a battery was removed")
            
            # if the battery was under testing, we interrupt the test, and open the relay
            if last_testing:
                print("test interrupted")
                last_testing = False
                open_relay(slot_id, slot_infos)
                
        # ============= Case 4 ============= 
        # if
        # - the preceding voltage was 0(+delta)
        # - and now we have > 0(+delta)
        # this means that a battery was inserted in the slot
        # - the voltage is > min_charged_voltage: the battery is charged, we test it
        # - the voltage is < min_charged_voltage: the battery is not fully charged, we don't test it
        #   a warning shall be sent, only once
        if (
            (last_voltage < voltage_empty_slot)
            and (voltage > voltage_empty_slot)
        ):
            
            # print("case 4, a battery was inserted")

            last_testing_session = float(last_testing_session) + 1
            
            if voltage > min_charged_voltage:
                print("The battery is charged, starting test")
                last_testing = True
                close_relay(slot_id, slot_infos)
                
            elif voltage > discharged_voltage:
                # print("The battery is not fully charged, not starting test")
                pass
            else:
                # print("The battery is discharged, not starting test")
                pass
            
        # ============= Case 6 ============= 
        # if
        # - the preceding voltage was > 0 and < discharged_voltage
        # - and now we still have > 0 and < discharged_voltage
        # this means that the slot is still filled with an empty battery
        if (
            (last_voltage > voltage_empty_slot)
            and (last_voltage < discharged_voltage)
            and (voltage > voltage_empty_slot)
            and (voltage < discharged_voltage)
        ):
            # print("case 6, still empty battery")
            pass
        
        timenow = datetime.now()
        if last_testing == True:
            delta_t = (timenow - pd.to_datetime(df_slots_history[df_slots_history.slot_id == slot_id].iloc[-1].time)) / pd.Timedelta(1, "s")
            mah = round(last_mah + voltage / R / 3600 * 1000 * delta_t, 3)
        voltage = round(voltage, 3)
        
        slot_measure = pd.Series(
                data=[timenow, slot_id, voltage, last_testing, last_testing_session, mah],
                index=['time', 'slot_id', 'voltage', 'testing', 'testing_session', 'spent_mah']
            )
        df_slots_history = df_slots_history.append(slot_measure, ignore_index=True)
        
        df = pd.DataFrame(slot_measure)
        df[0] = df[0].astype(str)

        # if not ( (voltage < voltage_empty_slot) and (last_voltage < voltage_empty_slot) ):
        if True:
            if os.path.isfile(csv_file):
                df.T.to_csv(csv_file, mode='a', header=False, index=False)
            else:
                if not os.path.exists("output"):
                    os.mkdir("output")
                df.T.to_csv(csv_file, index=False)

        if last_testing == True:
            print('batt ' + str(slot_id) + ": " + str(last_voltage) + "/" + str(voltage))
    
    if first_measure:
        # we remove the data created by the initialization function
        # we did not remove it before, because we need it to calculate if a test is starting
        df_slots_history = df_slots_history.iloc[4:]

    return df_slots_history

