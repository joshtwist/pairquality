from __future__ import print_function
import pickle
import os.path
import sys
import time
import socket
import importlib
from datetime import datetime

from google.oauth2 import service_account
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

args_count = len(sys.argv) - 1

if args_count > 0 and sys.argv[1] == 'mock':
    board_service = importlib.import_module('board_service_mock')
else:
    board_service = importlib.import_module('board_service')

board_service.init()

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

SPREADSHEET_ID = '1zSe0sMCBItdgZNqvWFC5JvJgqTDpHuC6ibnsdur9KDk'
BASELINE_RANGE = 'Baselines!A2:E'
READINGS_RANGE = 'Readings!A2:F'
CREDENTIALS_FILE_NAME = 'credentials.json'


def dt_string():
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def getSheets():
    creds = service_account.Credentials.from_service_account_file(CREDENTIALS_FILE_NAME, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=creds)
    sheets = service.spreadsheets()
    return sheets

def insertBaseline(baselines, ip):
    body = {
            "majorDimension": "ROWS",
            "values": [
                [baselines['serial'], dt_string(), baselines['eCO2'], baselines['TVOC'], ip]
            ]
        }
    
    request = getSheets().values().append(range=BASELINE_RANGE, spreadsheetId=SPREADSHEET_ID, insertDataOption='INSERT_ROWS', valueInputOption='RAW', body=body)
    response = request.execute()


def getBaselinesFromSheet(serial):
    rows = getSheets().values().get(spreadsheetId=SPREADSHEET_ID, range=BASELINE_RANGE).execute().get('values')

    if not rows:
        return None

    else:
        print('%s rows found' % len(rows))
        cursor = 0
        for row in rows:
            if (row[0] == serial):
                range = "Baselines!A%s:E" % (2+cursor)
                return {
                    'found_range': range,
                    'values': row
                }
            cursor = cursor + 1

    return None

def writeBaseline(baselines, ip):
    
    sheet_scan = getBaselinesFromSheet(baselines['serial'])

    if not sheet_scan:
        print('no matching data found... creating row')
        insertBaseline(baselines, ip)
        print('created new row for %s' % baselines['serial'])

    else:
        range = sheet_scan['found_range']

        body = {
                "majorDimension": "ROWS",
                "values": [
                    [baselines['serial'], dt_string(), baselines['eCO2'], baselines['TVOC'], ip]
                ]
            }

        request = getSheets().values().update(range=range, spreadsheetId=SPREADSHEET_ID, valueInputOption='RAW', body=body)
        response = request.execute()
        print('updated range %s' % range)
            

def writeReading(readings):

    body = {
        "majorDimension": "ROWS",
        "values": [
            [readings['serial'], dt_string(), readings['eCO2'], readings['TVOC'], readings['temperature'], readings['pressure'], readings['humidity']],  # new row
        ],
    }

    request = getSheets().values().append(range=READINGS_RANGE, spreadsheetId=SPREADSHEET_ID, insertDataOption='INSERT_ROWS', valueInputOption='RAW', body=body)
    response = request.execute()

    output = "Updated readings: {0:.2f} C, {1:.2f} hPa, {2:.2f} %RH, {3:.0f} CO2 ppm, {4:.0f} VOC ppb".format(
        readings['temperature'], readings['pressure'], readings['humidity'], readings['eCO2'], readings['TVOC'])
    print(output)
    
def updateDisplay(readings):
    
    co2 = readings['eCO2']
    now = datetime.now()
    message = "{3} {2:.1f}c\r\n{0:.0f}ppm {1:.0f}ppb".format(readings['eCO2'], readings['TVOC'], readings['temperature'], now.strftime("%H:%M%p"))
    print(message)
    
    if co2 > 2000:
        board_service.lcd_set_backlight_hex(0xFF8C00) #orange
    elif co2 > 1000:
        board_service.lcd_set_backlight_hex(0xFF0000) #bright red
    else:
        board_service.lcd_set_backlight_hex(0xFFFFFF) #bright white
        
    board_service.lcd_clear()
    board_service.lcd_write(message)

def main():
    
    board_service.lcd_clear()
    board_service.lcd_set_backlight_hex(0xA020F0) #violet

    sec_gap = 60 # default - how many seconds between readings
    baseline_frequency = 60 # default - how many readings between baseline updates
    
    board_service.lcd_write('Frequency %ss\r\nBaseline %s ' % (sec_gap, baseline_frequency))

    if args_count > 1:
        sec_gap = int(sys.argv[2])

    if args_count > 2:
        baseline_frequency = int(sys.argv[3])

    print("Initialized with writing delay %ss and baseline frequency of every %s reads" % (sec_gap, baseline_frequency))

    loop_counter = 0
    write_counter = 0

    serial = board_service.get_readings()['serial']

    # read baselines from spreadsheet if available
    sheet_scan = getBaselinesFromSheet(serial)
    
    if sheet_scan != None:
        row = sheet_scan['values']
        eCO2 = row[2]
        TVOC = row[3]
        board_service.set_board_baselines(eCO2, TVOC)

    while True:

        loop_counter += 1

        readings = board_service.get_readings()
        updateDisplay(readings)

        if (loop_counter >= sec_gap):
            writeReading(readings)
            write_counter += 1
            loop_counter = 0

            if (write_counter >= baseline_frequency):
                baselines = board_service.get_baselines()
                writeBaseline(baselines, get_ip())
                write_counter = 0

        time.sleep(1)

if __name__ == '__main__':
    main()
