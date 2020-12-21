import random

def init():
    print('⚠️ WARNING - initiated the mock Board Service ⚠️')

def get_readings():
    return {
        'serial': 'MOCK_fake_unit',
        'eCO2': 'MOCK_%s' % random.randint(400,8000),
        'TVOC': 'MOCK_%s' % random.randint(0, 25000),
        'temperature': 'MOCK_%s' % random.randint(21, 40),
        'pressure': 'MOCK_%s' % random.randint(1000,2000),
        'humidity': 'MOCK_%s' % random.randint(0,50)
    }

def get_baselines():
    return {
        'serial': 'MOCK_fake_unit',
        'eCO2': 'MOCK_0x%s' % random.randint(100,999),
        'TVOC': 'MOCK_0x%s' % random.randint(100,999)
    }

def set_board_baselines( eCO2, TVOC):
    print('fake call to set board baseline %s %s' % (eCO2, TVOC))


def get_serial():
    return 'MOCK_fake_unit'