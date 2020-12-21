# Welcome to the pAirQuality project

This is a simple project for the raspberry pi that allows you to build your own air quality sensor at home using stock components from sites like sparkfun.com

What you'll need

* Raspberry Pi
* SGP 30 Air Quality sensor
* BME 680 Environment sensor

To get started you'll need to hook both up to the SDA and SCL pins of your Raspberry Pi (I use the Qwiic connector for the SGP 30 and chain this onto the pimaroni BME680).

For anything to work you'll need to enable SCL and I2C on your Pi:

1. Pi Menu > Preferences > Raspberry Pi Configuration > Interfaces (Tab) 
2. Enable SCL and I2C
3. Install the packages for the two components
  * sudo pip3 install adafruit-circuitpython-sgp30
  * sudo pip3 install bme680

Tutorials for these two boards are available here:
* https://learn.adafruit.com/adafruit-sgp30-gas-tvoc-eco2-mox-sensor/circuitpython-wiring-test
* https://learn.pimoroni.com/tutorial/sandyj/getting-started-with-bme680-breakout

## Example script

    import time
    import board
    import busio
    import bme680
    import adafruit_sgp30

    i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)
    
    # Create library object on our I2C port
    sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c)
    sensor = bme680.BME680()

    print("SGP30 serial #", [hex(i) for i in sgp30.serial])

    sgp30.iaq_init()
    sgp30.set_iaq_baseline(0x8973, 0x8AAE)

    elapsed_sec = 0

    while True:
        #print("eCO2 = %d ppm \t TVOC = %d ppb" % (sgp30.eCO2, sgp30.TVOC))
        time.sleep(1)
        elapsed_sec += 1
        if elapsed_sec > 10:
            elapsed_sec = 0
            print(
                "**** Baseline values: eCO2 = 0x%x, TVOC = 0x%x"
                % (sgp30.baseline_eCO2, sgp30.baseline_TVOC)
            )
        if sensor.get_sensor_data():
            output = "{0:.2f} C, {1:.2f} hPa, {2:.2f} %RH, {3:.0f} CO2 ppm, {4:.0f} VOC ppb".format(sensor.data.temperature, sensor.data.pressure, sensor.data.humidity, sgp30.eCO2, sgp30.TVOC)
            print(output)
