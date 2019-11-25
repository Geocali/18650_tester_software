# Raspberry -based, 4-slots 18650 battery tester

An open source 18650 battery tester that discharges 4 batteries into 4 resistors, record the current flowing each second, and deducing the total capacity of the battery.

Just put the charged battery in a slot, and the test starts automatically.

You can follow the status of all the batteries in your browser, thanks to an Angular app:

![batteries dashboard](batteries_testing.png)

## List of material

- 1x raspberry pi
- 1x 4-channel 5V relay
- 4x 4Ohm 5W resistors
- 1x MCP3008 Analog numeric converter
- 1x 4 slots battery holder

## Wiring schematics

![schematics](schematic.svg)

## Structure of the program

The program is composed of 
- a python script that periodically records the voltages, deduce the current and save them in a Mariadb database
- a Flask api that retrieves data from the database
- an Angular front end that shows the batteries dashboard

## Run it

- Prepare the raspberry and run the backend : follow the instructions in `flaskapp/README.md`
- Install and run the front end : follow the instructions in `angularapp/README.md`

You can also run the back end in a non-raspberry computer, as an emulation has been created in `flaskapp/tester.py`, in order to ease the developments.