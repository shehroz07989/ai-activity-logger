import sqlite3

def trace_steps(request_id=None,step_name=None,step_order=None,standard_response=None):
    if standard_response != None:
        status = standard_response["status"]
        error = standard_response["error"]
    else:
        status = "pending"
        error = None
    conn = sqlite3.connect("sqlite/system.db")
    cursor = conn.cursor()
    cursor.execute("""
                    INSERT INTO trace(status,request_id,step_name,step_order,error)
                   VALUES (?,?,?,?,?)
                   ON CONFLICT (request_id, step_name, step_order) 
                   DO UPDATE SET
                   status = excluded.status,
                   error = excluded.error
                    """,(status,request_id,step_name,step_order,error))
    conn.commit()
    conn.close()