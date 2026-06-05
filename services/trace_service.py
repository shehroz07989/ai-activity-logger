import sqlite3
from general_functions.utils import build_response
def workflow_response_normalizer_for_trace(data):
    payload = {
        "status":data["status"],
        "api_workflow_attempts": data["result"]["attempts"],
        "error": data["error"]["detail"]
    }
    
    return payload
def trace_steps(request_id=None,step_name=None,step_order=None,standard_response=None):
    if standard_response != None:
        status = standard_response["status"]
        error = standard_response["error"]
        if "api_workflow_attempts" in standard_response:
            api_workflow_attempts = standard_response["api_workflow_attempts"]
        else:
            api_workflow_attempts = None
    else:
        status = "pending"                     
        error = None
        api_workflow_attempts = None
        
    conn = sqlite3.connect("sqlite/system.db")
    cursor = conn.cursor()
    cursor.execute("""
                    INSERT INTO trace(status,request_id,step_name,step_order,error,api_workflow_attempts)
                   VALUES (?,?,?,?,?,?)
                   ON CONFLICT (request_id, step_name, step_order) 
                   DO UPDATE SET
                   status = excluded.status,
                   error = excluded.error,
                   api_workflow_attempts = excluded.api_workflow_attempts
                    """,(status,request_id,step_name,step_order,error,api_workflow_attempts))
    conn.commit()
    conn.close()