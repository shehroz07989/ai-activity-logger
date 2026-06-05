import time
from domain_specific_functions.api_call_functions import call_api
from services.attempts_trace import trace_attempts
from services.retry_policy import retry_policy

def api_call_workflow(data):
    called_api = call_api(data)
    current_attempts = 1 
    
    if called_api["status"] != "success": 
        trace_attempts(step_name="api_call_workflow",attempt=current_attempts,data=called_api)
        retry_policy_response = retry_policy(called_api["error"])
        if retry_policy_response["result"]["action"] == "retry":
            retry = retry_policy_response["result"]["payload"]["max_attempts"]
            while current_attempts < retry:
                current_attempts += 1
                called_api = call_api(data)
                trace_attempts(step_name="api_call_workflow",attempt=current_attempts,data=called_api)
                if called_api["status"] != "success":
                    retry_policy_response = retry_policy(called_api["error"])
                    if retry_policy_response["result"]["action"] == "retry":
                        time.sleep(2**current_attempts)
                        continue
                    elif retry_policy_response["result"]["action"] == "terminate":
                        break
                else:
                    called_api["result"] = {
                        "response": called_api["result"],
                        "attempts": current_attempts
                    }
                    return called_api
        
    called_api["result"] = {
                    "response": called_api["result"],
                    "attempts": current_attempts
                }
    return called_api