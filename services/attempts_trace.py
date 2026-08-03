
from sqlite.connection import get_connection


def trace_attempts(step_name,attempt,data,request_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO attempts(trace_id,step_name,attempt,status,error) VALUES (?,?,?,?,?)
            """ ,(request_id,step_name,attempt,data["status"],data["error"]["detail"]))
        conn.commit() # Transaction Policy must be separate in the future.

        

