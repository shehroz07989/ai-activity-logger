from general_functions.utils import validate
import sqlite3

def get_all_logs():
    conn = sqlite3.connect("sqlite/system.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
                SELECT * FROM logs 
                               """)
    row = cursor.fetchall()
    response = [] 
    for i in row:
        response.append(dict(i))

    return response


def get_log_by_id(user_id:int):
    validated = validate(user_id)
    if validated["status"] != "success":
        return "validation_failed"
    conn = sqlite3.connect("sqlite/system.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
                SELECT * FROM logs WHERE unique_id = ? 
                               """,(user_id,))
    try:
        response = cursor.fetchone()
        if response is None:
            return None
        response = dict(response)
        return response
    except sqlite3.Error as e:
        
        return "error_in_db"        
    finally:
        conn.close()