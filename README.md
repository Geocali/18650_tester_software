# Raspberry -based, 4-slots 18650 battery tester

This is an open source 18650 battery tester that discharges 4 batteries into 4 resistors, records the current flowing each second, and deduces the total capacity of the battery.

Just put the charged battery in a slot, and the test starts automatically if the battery is charged. You can then follow the test on curves updated automatically in a web page.

# Construction

## List of material

- 1x raspberry pi
- 1x 4-channel 5V relay
- 4x 4Ohm 5W resistors
- 1x MCP3008 Analog numeric converter
- 1x 4 slots battery holder
- 1x USB wifi dongle (optional)

## Wiring

![tester schematics](docs/schematic.svg)

# Set up your Raspberry

## Configure I2C

### Install the required libraries

```
sudo pip3 install --upgrade setuptools
sudo apt-get install -y python-smbus
sudo apt-get install -y i2c-tools
```

### Enable I2C

```
sudo raspi-config
```
In the menus, go to `Interfacing options`, then `I2C` and choose `YES`

Then, run

```
sudo reboot
sudo i2cdetect -y 1
```

## Configure SPI

Configure SPI with the following commands:

```
sudo raspi-config
Interfacing options / SPI / YES
sudo reboot
ls -l /dev/spidev*
```

## Install additional libraries
```
pip3 install -f requirements.txt
```

# Run the app

## Start the script that manages the testing of the batteries
```
python3 tester.py
```

## Start the Flask API
```
python3 app.py
```

# Develop
