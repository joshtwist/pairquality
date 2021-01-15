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
    global serlcd

    i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)
    
    sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c)
    sensor = bme680.BME680()
    serial = '-'.join(str(e) for e in sgp30.serial)
    sgp30.iaq_init()
    print('Initiated real Board Service for SGP30 Serial ', serial)

    lcd_i2c = busio.I2C(board.CSL, board.SDA)
    serlcd = Sparkfun_SerLCD_I2C(lcd_i2c)
    

def get_readings():
    attempts = 0
    while attempts < 3:
        try:
            # sensor.data.temperature, sensor.data.pressure, sensor.data.humidity
            # sgp30.eCO2, sgp30.TVOC
            if not sensor.get_sensor_data():
                print('get_sensor_data() failed')
            else:   
                return {
                    'serial': serial,
                    'eCO2': sgp30.eCO2,
                    'TVOC': sgp30.TVOC,
                    'temperature': sensor.data.temperature,
                    'pressure': sensor.data.pressure,
                    'humidity': sensor.data.humidity
                }
        except OSError as ose:
            attempts += 1
            print("get_readings attempt %s: %s" % (attempts, ose))
            time.sleep(0.1)

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
    attempts = 0
    while attempts < 3:
        try:
            serlcd.clear()
            return
        except OSError as ose:
            attempts += 1
            print("lcd_clear attempt %s: %s" % (attempts, ose))
            time.sleep(0.1)
            
def lcd_write(message):
    attempts = 0
    while attempts < 3:
        try:
            serlcd.write(message)
            return
        except OSError as ose:
            attempts += 1
            print("lcd_write attempt %s: %s" % (attempts, ose))
            time.sleep(0.1)

def lcd_set_backlight_hex(hex):
    attempts = 0
    while attempts < 3:
        try:
            serlcd.set_backlight(hex) 
            return
        except OSError as ose:
            attempts += 1
            print("lcd_set_backlight_hex attempt %s: %s" % (attempts, ose))
            time.sleep(0.1)