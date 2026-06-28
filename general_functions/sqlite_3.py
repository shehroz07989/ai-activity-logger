from general_functions.utils import build_response
import sqlite3
def execute_query_fetchone(query):
    try:
        conn = None
        conn = sqlite3.connect("sqlite/system.db",timeout=5)
        conn.row_factory =sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        if not result:
             return build_response(
                  status="success",
                  result=None
             )
        converted_result = dict(result)     
        
        return build_response(
            status="success",
            result=converted_result
                )
    except Exception as e:
        return build_response(
            status="failed",
            error=e
        )
    finally:
        if conn != None:
            conn.close()


def execute_query_fetchtall(query):
    try:
        conn = None
        conn = sqlite3.connect("sqlite/system.db",timeout=5)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        if not result:
             return build_response(
                  status="success",
                  result=None
             )
        converted_result = dict(result)
    
        
        return build_response(
            status="success",
            result=converted_result
        )
    
    except Exception as e:
        return build_response(
            status="failed",
            error=e
        )
    finally:
        if conn != None:
            conn.close()



def sqlite_error_checker(error):
    error_name = type(error).__name__
    if error_name == "OperationalError":
        return build_response(
            status="success",
            result={
                "name": error_name,
                "type": "temporary",
                "detail": str(error)
            }
        )
    if error_name == "ProgrammingError":
        return build_response(
            status="success",
            result={
                "name": error_name,
                "type": "permanent",
                "detail": str(error)
            }
        )
    if error_name == "IntegrityError":
        return build_response(
            status="success",
            result={
                "name": error_name,
                "type": "permanent",
                "detail": str(error)
            }
        )
    if error_name == "InterfaceError":
        return build_response(
            status="success",
            result={
                "name": error_name,
                "type": "permanent",
                "detail": str(error)
            }
        )
    else:
        return build_response(
            status="success",
            result={
                "name": error_name,
                "type": "permanent",
                "detail": str(error)
            }
        )




