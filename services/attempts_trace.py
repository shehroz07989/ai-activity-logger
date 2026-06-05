import sqlite3
def extract_trace_id():
    conn = sqlite3.connect("sqlite/system.db")
    cursor = conn.cursor()
    cursor.execute("""
            SELECT trace_id
        FROM trace
        ORDER BY trace_id DESC
        LIMIT 1
        """)
    row = cursor.fetchone()
    conn.close()
    trace_id = row[0]
    return trace_id

def trace_attempts(step_name,attempt,data):
    trace_id = extract_trace_id()
    conn = sqlite3.connect("sqlite/system.db")
    cursor = conn.cursor()
    cursor.execute("""
            INSERT INTO attempts(trace_id,step_name,attempt,status,error) VALUES (?,?,?,?,?)
            """ ,(trace_id,step_name,attempt,data["status"],data["error"]["detail"]))
    conn.commit()
    conn.close()

