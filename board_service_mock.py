import random
import time

def init():
    global serial 
    serial = 'MOCK_fake_unit'
    print('⚠️ WARNING - initiated the mock Board Service ⚠️ Serial: ', serial)

def get_readings():
    return {
        'serial': serial,
        'eCO2': random.randrange(0,2),
        'TVOC': random.randrange(0,2),
        'temperature': random.randrange(0,2),
        'pressure': random.randrange(0,2),
        'humidity': random.randrange(0,2)
    }

def get_baselines():
    return {
        'serial': serial,
        'eCO2': random.randrange(0,2),
        'TVOC': random.randrange(0,2)
    }

def set_board_baselines( eCO2, TVOC):
    print('fake call to set board baseline %s %s' % (eCO2, TVOC))


def get_serial():
    return serial

def lcd_clear():
    print("<LCD CLEAR>")
    time.sleep(0.1)

def lcd_write(message):
    print("LCD: %s " % message)

def lcd_set_backlight_hex(hex):
    print("<LCD BACKLIGHT %s>" % hex)