# Welcome to the pAirQuality project

This is a simple project for the raspberry pi that allows you to build your own air quality sensor at home using stock components from sites like sparkfun.com

What you'll need

* Raspberry Pi
* SGP 30 Air Quality sensor
* BME 680 Environment sensor
* Sparkfun SerLCD (Qwiic version)

To get started you'll need to hook both up to the SDA and SCL pins of your Raspberry Pi (I use the Qwiic connector for the SGP 30 and chain this onto the pimaroni BME680).

For anything to work you'll need to enable SCL and I2C on your Pi:

1. Pi Menu > Preferences > Raspberry Pi Configuration > Interfaces (Tab) 
2. Enable SCL and I2C
3. Install the packages for the two components
  * sudo pip3 install RPI.GPIO
  * sudo pip3 install adafruit-blinka
  * sudo pip3 install adafruit-circuitpython-sgp30
  * sudo pip3 install bme680
  * sudo pip3 install sparkfun-circuitpython-serlcd
  * sudo pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

Tutorials for these two boards are available here:
* https://learn.adafruit.com/adafruit-sgp30-gas-tvoc-eco2-mox-sensor/circuitpython-wiring-test
* https://learn.pimoroni.com/tutorial/sandyj/getting-started-with-bme680-breakout
* https://github.com/fourstix/Sparkfun_CircuitPython_SerLCD

## Kicking off the process

Recommend using the bash script (`run.sh`) to restart the python script in the event of a failure and `nohup` to dump the output to file for investigation later. 

` nohup ./run.sh &

This will dump the logs in a file called nohup.out. If you see a permission denied error, make sure the run.sh file is executable:

` chmod +x ./run.sh
