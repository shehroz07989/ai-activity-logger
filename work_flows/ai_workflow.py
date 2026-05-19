from general_functions.utils import parse_json,build_response
import time
from domain_specific_functions.ai_functions import validate_ai_response,ai_call


def ai_call_proccess(data):
    
    can_continue = True
    attempts = 0
    while attempts < 3:
        
        loop_status = "success"
        attempts += 1

        ai_called = ai_call(data)
        
        errors = {"time_out", "connection_error"}
        if ai_called["status"] == "success":            
            break
        elif ai_called["error_type"] == "status_code":
            status_code = ai_called["status_code"]
            if 500 <= status_code <= 599:
                loop_status = "retry_exhausted"
                time.sleep(attempts ** 2)
                continue
            else:
                loop_status = "non_retryable"
                break
        elif ai_called["error"] in errors:
            
            loop_status = "retry_exhausted"
            time.sleep(attempts ** 2)
            continue
        else:
            loop_status = "non_retryable"
            break
        
    if loop_status != "success":
            can_continue =False
            return  build_response(
                status="ai_call_failed",
                user_input=None,
                result=None,
                error=ai_called["error"]
            )
            
    
    if can_continue:
        parsed_json = parse_json(ai_called["result"])
        if parsed_json["status"] != "success":
            can_continue = False
            return  build_response(
                status="ai_call_failed",
                user_input=None,
                result=None,
                error=parsed_json["error"]
            )

    
    if can_continue:
        validate_parsed_json = validate_ai_response(parsed_json["result"])
        if validate_parsed_json["status"] != "success":
            can_continue = False
            return  build_response(
                status="ai_call_failed",
                user_input=None,
                result=None,
                error=validate_parsed_json["error"]
            )
    if can_continue:
        
        return  build_response(
                status="success",
                user_input=None,
                result=validate_parsed_json["result"],
                error=None
            )
