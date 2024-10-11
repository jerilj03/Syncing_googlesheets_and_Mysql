import datetime
from logger import log_info, log_error
from googleapiclient.discovery import build
from google.oauth2 import service_account
import datetime



# Google Sheets configuration
SHEET_ID = '12JOF2VyoMSAoVzIgNzXT2zzBoQpOyHR4bDKVGifSRZw'
RANGE_NAME = 'Sheet1!A:D'
LAST_SYNC_CELL = 'Sheet1!E1'


def read_sheet_data(sheet_service):
    result = sheet_service.values().get(spreadsheetId=SHEET_ID, range=RANGE_NAME).execute()
    values = result.get('values', [])
    
    # Ensure each row has 4 columns
    formatted_data = []
    for row in values:
        if len(row) < 4:
            row.extend([''] * (4 - len(row)))
        formatted_data.append(tuple(row))  # Convert each row to a tuple

    return formatted_data

def update_sheet_data(sheet_service, data):
    values = [list(row) for row in data]  # Convert tuples to lists
    body = {
        'values': values
    }
    result = sheet_service.values().update(
        spreadsheetId=SHEET_ID,
        range=RANGE_NAME,
        valueInputOption='RAW',
        body=body
    ).execute()
    log_info("%d cells updated in Google Sheets.", result.get('updatedCells'))

def get_last_sync_time_from_sheet(sheet_service):
    result = sheet_service.values().get(spreadsheetId=SHEET_ID, range=LAST_SYNC_CELL).execute()
    last_sync_time_str = result.get('values', [[None]])[0][0]
    if last_sync_time_str:
        return datetime.datetime.strptime(last_sync_time_str, '%Y-%m-%dT%H:%M:%S.%fZ')
    else:
        return datetime.datetime.min

def update_last_sync_time_in_sheet(sheet_service, timestamp):
    body = {
        'values': [[timestamp.strftime('%Y-%m-%dT%H:%M:%S.%fZ')]]
    }
    sheet_service.values().update(
        spreadsheetId=SHEET_ID,
        range=LAST_SYNC_CELL,
        valueInputOption='RAW',
        body=body
    ).execute()


def delete_sheet_data(sheet_service, start_row, end_row):
    requests = [
        {
            'deleteRange': {
                'range': {
                    'sheetId': SHEET_ID,
                    'startRowIndex': start_row,
                    'endRowIndex': end_row,
                },
                'shiftDimension': 'ROWS'
            }
        }
    ]
    body = {
        'requests': requests
    }
    result = sheet_service.spreadsheets().batchUpdate(
        spreadsheetId=SHEET_ID,
        body=body
    ).execute()
    log_info("Deleted rows %d to %d.", start_row, end_row)