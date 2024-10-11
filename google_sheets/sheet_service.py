# from googleapiclient.discovery import build
# from google.oauth2 import service_account

# # Google Sheets configuration
# SHEET_ID = '12JOF2VyoMSAoVzIgNzXT2zzBoQpOyHR4bDKVGifSRZw'
# SERVICE_ACCOUNT_FILE = r'C:\Users\jeril\Desktop\superjoin_assgn\google_sheets\mysqlsheets-435615-fa7d6f85d058.json'
# SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# def get_sheets_service():
#     credentials = service_account.Credentials.from_service_account_file(
#         SERVICE_ACCOUNT_FILE, scopes=SCOPES
#     )
#     return build('sheets', 'v4', credentials=credentials).spreadsheets()


from googleapiclient.discovery import build
from google.oauth2 import service_account

# Google Sheets configuration
SHEET_ID = '12JOF2VyoMSAoVzIgNzXT2zzBoQpOyHR4bDKVGifSRZw'
SERVICE_ACCOUNT_FILE = r'C:\Users\jeril\Desktop\superjoin_assgn\google_sheets\mysqlsheets-435615-fa7d6f85d058.json'
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive.metadata.readonly'  # Add Google Drive scope
]

def get_sheets_service():
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    return build('sheets', 'v4', credentials=credentials).spreadsheets()

def get_drive_service():
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    return build('drive', 'v3', credentials=credentials)

def get_last_modified_time(sheet_id):
    drive_service = get_drive_service()
    file_metadata = drive_service.files().get(fileId=sheet_id, fields="modifiedTime").execute()
    return file_metadata['modifiedTime']

if __name__ == "__main__":
    last_modified_time = get_last_modified_time(SHEET_ID)
    print(f"Last modified time of the Google Sheet: {last_modified_time}")
