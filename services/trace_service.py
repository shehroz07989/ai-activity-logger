import sqlite3
def workflow_response_normalizer_for_trace(data):
    payload = {
        "status":data["status"],
        "workflow_attempts": data["result"]["attempts"],
        "error": data["error"]["detail"]
    }
    
    return payload
def trace_steps(request_id=None,step_name=None,step_order=None,standard_response=None):
    if standard_response != None:
        status = standard_response["status"]
        error = standard_response["error"]
        if "workflow_attempts" in standard_response:
            workflow_attempts = standard_response["workflow_attempts"]
        else:
            workflow_attempts = None
    else:
        status = "pending"                     
        error = None
        workflow_attempts = None
        
    conn = sqlite3.connect("sqlite/system.db")
    cursor = conn.cursor()
    cursor.execute("""
                    INSERT INTO trace(status,request_id,step_name,step_order,error,workflow_attempts)
                   VALUES (?,?,?,?,?,?)
                   ON CONFLICT (request_id, step_name, step_order) 
                   DO UPDATE SET
                   status = excluded.status,
                   error = excluded.error,
                   workflow_attempts = excluded.workflow_attempts
                    """,(status,request_id,step_name,step_order,error,workflow_attempts))
    conn.commit()
    conn.close() 