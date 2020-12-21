from __future__ import print_function
import pickle
import os.path
import time
import importlib
from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


board_service = importlib.import_module('board_service_mock')
# board_service = importlib.import_module('board_service')

board_service.init()

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

SPREADSHEET_ID = '1zSe0sMCBItdgZNqvWFC5JvJgqTDpHuC6ibnsdur9KDk'
BASELINE_RANGE = 'Baselines!A2:D'
READINGS_RANGE = 'Readings!A2:F'
CREDENTIALS_FILE_NAME = 'credentials.json'

def dt_string():
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

def getSheets():
    creds = service_account.Credentials.from_service_account_file(CREDENTIALS_FILE_NAME, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=creds)
    sheets = service.spreadsheets()
    return sheets

def insertBaseline(baselines):
    body = {
            "majorDimension": "ROWS",
            "values": [
                [baselines['serial'], dt_string(), baselines['eCO2'], baselines['TVOC']]
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
                range = "Baselines!A%s:D" % (2+cursor)
                return {
                    'found_range': range,
                    'values': row
                }
            cursor = cursor + 1

    return None

def writeBaseline(baselines):
    
    sheet_scan = getBaselinesFromSheet(baselines['serial'])

    if not sheet_scan:
        print('no matching data found... creating row')
        insertBaseline(baselines)
        print('created new row for %s' % baselines['serial'])

    else:
        range = sheet_scan['found_range']

        body = {
                "majorDimension": "ROWS",
                "values": [
                    [baselines['serial'], dt_string(), baselines['eCO2'], baselines['TVOC']]
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

    print('updated readings')

def main():

    sec_gap = 60 # 60
    baseline_frequency = 60 # 60

    counter = 0
    serial = board_service.get_readings()['serial']

    # read baselines from spreadsheet if available
    sheet_scan = getBaselinesFromSheet(serial)
    
    if sheet_scan != None:
        row = sheet_scan['values']
        eCO2 = row[2]
        TVOC = row[3]
        board_service.set_board_baselines(eCO2, TVOC)

    while True:

        readings = board_service.get_readings()
        writeReading(readings)

        counter += 1

        if (counter >= baseline_frequency):
            baselines = board_service.get_baselines()
            writeBaseline(baselines)
            counter = 0

        time.sleep(sec_gap)

if __name__ == '__main__':
    main()
