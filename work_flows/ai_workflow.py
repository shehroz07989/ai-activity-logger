from general_functions.utils import parse_json,build_response
import time
from domain_specific_functions.ai_functions import validate_ai_response,ai_call
from services.attempts_trace import trace_attempts
from services.retry_policy import retry_policy


def ai_call_workflow(data):
    ai_called = ai_call(data)
    current_attempts = 1

    if ai_called["status"] != "success":
        trace_attempts(step_name="ai_call_workflow",attempt=current_attempts,data=ai_called)
        retry_policy_response = retry_policy(ai_called["error"])#In retry Policy Unknown "type" bug Remains etc "temporary","permanent"
        if retry_policy_response["result"]["action"] == "retry":
            retry = retry_policy_response["result"]["payload"]["max_attempts"] 
            while current_attempts < retry:
                current_attempts += 1
                ai_called = ai_call(data)
                trace_attempts(step_name="ai_call_workflow",attempt=current_attempts,data=ai_called)
                if ai_called["status"] != "success":
                    if current_attempts == retry:
                        return build_response(
                            status="ai_failed",
                            result={
                                    "response": ai_called["result"],
                                    "attempts": current_attempts
                                        },
                            error=ai_called["error"]
                                    
                        )
                    retry_policy_response = retry_policy(ai_called["error"])
                    if retry_policy_response["result"]["action"] == "terminate":
                        return build_response(
                            status="ai_failed",
                            result={
                                    "response": ai_called["result"],
                                    "attempts": current_attempts
                                        },
                            error=ai_called["error"]
                                )
                    if retry_policy_response["result"]["action"] == "retry":
                        time.sleep(2**current_attempts)
                        continue
                    
        

    parsed_json = parse_json(ai_called["result"])
    
    if parsed_json["status"] != "success":
        return  build_response(
            status="ai_workflow_failed",
            user_input=None,
            result={
                        "response": ai_called["result"],
                        "attempts": current_attempts
                    },
            error=parsed_json["error"]
        )
    validate_parsed_json = validate_ai_response(parsed_json["result"])
    if validate_parsed_json["status"] != "success":
        return  build_response(
            status="ai_workflow_failed",
            user_input=None,
            result={
                        "response": ai_called["result"],
                        "attempts": current_attempts
                    },
            error=validate_parsed_json["error"]
        )

    ai_called["result"] = {
                            "response": ai_called["result"],
                            "attempts": current_attempts
                        }
    return ai_called


