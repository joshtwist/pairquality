import board
import busio
import time
import bme680
import adafruit_sgp30
from sparkfun_serlcd import Sparkfun_SerLCD_I2C

def init():
    
    global sgp30
    global sensor
    global serial

    i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)
    serlcd = Sparkfun_SerLCD_I2C(i2c)
    sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c)
    sensor = bme680.BME680()
    serial = '-'.join(str(e) for e in sgp30.serial)
    sgp30.iaq_init()
    print('Initiated real Board Service for SGP30 Serial ', serial)

def get_readings():
    # sensor.data.temperature, sensor.data.pressure, sensor.data.humidity
    # sgp30.eCO2, sgp30.TVOC
    if not sensor.get_sensor_data():
        print('get_sensor_data() failed')
        
    return {
        'serial': serial,
        'eCO2': sgp30.eCO2,
        'TVOC': sgp30.TVOC,
        'temperature': sensor.data.temperature,
        'pressure': sensor.data.pressure,
        'humidity': sensor.data.humidity
    }

def get_baselines():
    # sgp30.baseline_eCO2, sgp30.baseline_TVOC
    return {
        'serial': serial,
        'eCO2': hex(sgp30.baseline_eCO2),
        'TVOC': hex(sgp30.baseline_TVOC)
    }

def set_board_baselines(eCO2, TVOC):

    # convert strings to hex if necessary
    if isinstance(eCO2, str):
        eCO2 = int(eCO2, 16)

    if isinstance(TVOC, str):
        TVOC = int(TVOC, 16)

    sgp30.set_iaq_baseline(eCO2, TVOC)
    print('set_iaq_baseline %s %s' % (hex(eCO2), hex(TVOC)))
    
def get_serial():
    return serial


def lcd_clear():
    serlcd.clear()
    time.sleep(0.1)

def lcd_write(message):
    serlcd.write(message)

def lcd_set_backlight_hex(hex):
    serlcd.set_backlight(hex) 