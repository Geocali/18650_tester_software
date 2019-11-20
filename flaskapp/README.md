# Installation

## Configure I2C
sudo pip3 install --upgrade setuptools
sudo apt-get install -y python-smbus
sudo apt-get install -y i2c-tools

sudo raspi-config
Interfacing options / I2C / YES

sudo reboot
sudo i2cdetect -y 1

## Configure SPI
sudo raspi-config
Interfacing options / SPI / YES
sudo reboot
ls -l /dev/spidev*

## Install libraries
pip3 install -f requirements.txt
sudo apt-get install libmariadbclient-dev

## Test I2C and SPI libraries
'''import board
import digitalio
import busio
 
print("Hello blinka!")
 
# Try to great a Digital input
pin = digitalio.DigitalInOut(board.D4)
print("Digital IO ok!")
 
# Try to create an I2C device
i2c = busio.I2C(board.SCL, board.SDA)
print("I2C ok!")
 
# Try to create an SPI device
spi = busio.SPI(board.SCLK, board.MOSI, board.MISO)
print("SPI ok!")
 
print("done!")'''

Run mcp3008_differential_simpletest.py to see if the MCP3008 library works

# Control Relay
https://tutorials-raspberrypi.com/raspberry-pi-control-relay-switch-via-gpio/
https://pinout.xyz/

# MCP3008
https://pimylifeup.com/raspberry-pi-adc/

# Run the app

## Setup the database
sudo apt-get install mariadb-server
sudo mysql -u root
use mysql;
update user set plugin='' where User='root';
flush privileges;
\q
mysql_secure_installation
mysql -u root -p (caramel)
CREATE DATABASE battery_schema;
\q

## Start the script that manages the testing of the batteries
python3 tester.py

## Start the Flask API
python3 app.py
