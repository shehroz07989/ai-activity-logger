import time
from general_functions.sqlite_3 import execute_query_fetchone,execute_query_fetchtall,sqlite_error_checker
from general_functions.utils import build_response
from services.retry_policy import retry_policy
def sqlite_execution_service(query,fetch_mode):
    current_attempts = 0
    while True:    
        current_attempts += 1
        if fetch_mode == "all":
            fetched_data = execute_query_fetchtall(query)  
                    
        elif fetch_mode == "one":
            fetched_data = execute_query_fetchone(query)
        else:
             return build_response(
                status="failed",
                error="fetch_mode_unknown",
                result=None
             )
            
          
        if fetched_data["status"] != "success":
            error_checked = sqlite_error_checker(fetched_data["error"])
            if error_checked["status"] != "success":
                raise  ValueError("sqlite_error_checker_failed_in_monitoring_service")
            retry_policy_response = retry_policy(error_checked["result"])
            if retry_policy_response["result"]["action"] == "retry":
                retry = retry_policy_response["result"]["payload"]["max_attempts"]
                if current_attempts == retry:
                    return build_response(
                        status="failed",
                        error=error_checked["result"]["name"],
                        result=None
                    )
                time.sleep(2)
                continue
            elif retry_policy_response["result"]["action"] == "terminate":
                return build_response(
                    status="failed",
                    error=error_checked["result"]["name"],
                    result=None
                )
            

            
        elif fetched_data["result"] == None:
                return build_response(
                     status="success",
                     result="data_not_exist"
                ) 
        return build_response(
                status="success",
                result=fetched_data["result"]
            )
        


