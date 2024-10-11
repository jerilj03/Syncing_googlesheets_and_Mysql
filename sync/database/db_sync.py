import mysql.connector
from logger import log_info, log_error
from database.db_service import get_db_connection
import datetime

def read_db_data(last_sync_time):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT col1, col2, col3, col4 FROM test_table WHERE last_modified > %s", (last_sync_time,))
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows

def update_db_data(data):
    connection = get_db_connection()
    cursor = connection.cursor()
    
    # Extract current keys from the data
    current_keys = {row[0] for row in data}  # Assuming col1 is the primary key
    
    # Identify outdated keys that need to be deleted
    cursor.execute("SELECT col1 FROM test_table")
    all_keys = {row[0] for row in cursor.fetchall()}
    outdated_keys = all_keys - current_keys
    
    # Delete rows with outdated keys
    if outdated_keys:
        delete_query = "DELETE FROM test_table WHERE col1 IN (%s)" % ','.join(['%s'] * len(outdated_keys))
        cursor.execute(delete_query, tuple(outdated_keys))
    
    # Prepare and execute the insert/update query
    insert_query = """
    INSERT INTO test_table (col1, col2, col3, col4)
    VALUES (%s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
    col2=VALUES(col2), col3=VALUES(col3), col4=VALUES(col4), last_modified=NOW()
    """
    
    try:
        cursor.executemany(insert_query, data)
        connection.commit()
        log_info("Successfully updated %d rows in the database.", cursor.rowcount)
    except mysql.connector.Error as err:
        log_error("Error: %s", err)
    finally:
        cursor.close()
        connection.close()


def get_last_db_update_time():
    """
    Fetches the timestamp of the most recent update in the database.
    Assumes there is a 'last_modified' or equivalent column in the database.
    """
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        # Assuming your table has a column called 'last_modified' to track updates
        query = "SELECT MAX(last_modified) FROM test_table"  # Replace 'your_table_name' with the actual table name
        cursor.execute(query)
        result = cursor.fetchone()

        # If the table is empty or no updates have been made, return the minimum date
        if result[0] is None:
            return datetime.datetime.min
        
        return result[0]  # The latest timestamp from the 'last_modified' column

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return datetime.datetime.min  # Return the minimum date on error

    finally:
        cursor.close()
        connection.close()