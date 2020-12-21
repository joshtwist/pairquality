import random

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