import mysql.connector
from googleapiclient.discovery import build
from google.oauth2 import service_account

# Database connection configuration
# DB_HOST = 'Jeril_J'
DB_USER = 'root'
DB_PASSWORD = '1915'
DB_DATABASE = 'my_db'

# Google Sheets configuration
SHEET_ID = '12JOF2VyoMSAoVzIgNzXT2zzBoQpOyHR4bDKVGifSRZw'
RANGE_NAME = 'Sheet1!A:D'  # Adjust to match your sheet range

# Google Sheets API setup
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = r'C:\Users\jeril\Desktop\superjoin_assgn\google_sheets\mysqlsheets-435615-fa7d6f85d058.json'

# Create Google Sheets service
def get_sheets_service():
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    return build('sheets', 'v4', credentials=credentials).spreadsheets()

def get_db_connection():
    return mysql.connector.connect(
        # host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_DATABASE
    )

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

def read_db_data():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT col1, col2, col3, col4 FROM test_table")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows

def update_db_data(data):
    connection = get_db_connection()
    cursor = connection.cursor()
    
    # Optional reset
    # cursor.execute("DELETE FROM test_table")
    
    insert_query = """
    INSERT INTO test_table (col1, col2, col3, col4)
    VALUES (%s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
    col2=VALUES(col2), col3=VALUES(col3), col4=VALUES(col4)
    """
    
    try:
        cursor.executemany(insert_query, data)
        connection.commit()
        print(f"Successfully updated {cursor.rowcount} rows in the database.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        connection.close()

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
    print(f"{result.get('updatedCells')} cells updated in Google Sheets.")

def sync_google_sheet_to_db():
    sheet_service = get_sheets_service()
    sheet_data = read_sheet_data(sheet_service)
    print("Data from Google Sheets:", sheet_data)
    
    for row in sheet_data:
        if len(row) != 4:
            print(f"Error: Data row {row} does not match expected format (4 columns)")
            return
    
    db_data = read_db_data()
    print("Data from Database:", db_data)

    if sheet_data != db_data:
        print("Syncing Google Sheet -> Database")
        update_db_data(sheet_data)
    else:
        print("Google Sheet and Database are already in sync.")

def sync_db_to_google_sheet():
    sheet_service = get_sheets_service()
    db_data = read_db_data()
    
    formatted_data = [list(row) for row in db_data]
    
    sheet_data = read_sheet_data(sheet_service)

    if formatted_data != sheet_data:
        print("Syncing Database -> Google Sheet")
        update_sheet_data(sheet_service, formatted_data)
    else:
        print("Database and Google Sheet are already in sync.")

def sync_loop(a):
    if a==1:
        sync_google_sheet_to_db()
    if a==2:
        sync_db_to_google_sheet()

if __name__ == "__main__":
    print("Enter 1 to sync google sheets to db")
    print("Enter 2 to sync db to google sheets")
    a = int(input())
    sync_loop(a)
