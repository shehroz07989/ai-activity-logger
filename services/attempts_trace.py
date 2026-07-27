import sqlite3


def trace_attempts(step_name,attempt,data,request_id):
    conn = sqlite3.connect("sqlite/system.db")
    cursor = conn.cursor()
    cursor.execute("""
            INSERT INTO attempts(trace_id,step_name,attempt,status,error) VALUES (?,?,?,?,?)
            """ ,(request_id,step_name,attempt,data["status"],data["error"]["detail"]))
    conn.commit()
    conn.close()

