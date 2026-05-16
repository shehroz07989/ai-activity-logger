from utils import validate, call_api,filter_data,save_log,trace_data,parse_json,validate_ai_response
import uuid
from duplicate import ai_call
# -----------------Mene abi isme step+1 nhi lgayya chatgpt ka akhri mesage dekhna ha ussne kia kha ha -------------

def main():
    
    id = input("Enter id: ")
    request_id = str(uuid.uuid4())
    log_data = {
                "input": id,
                "cleaned_input": None,
                "status": None,
                "post_id": None,
                "error": None,
                "title": None,
                "raw_response": None,
                "attempts" : None,
                "request_id": request_id,
                "ai_generated": None,
                "ai_explanation": None
            }
    
    
    step = 0
    can_continue = True
    
    validated = validate(id)
    step += 1
    log_data["status"] = validated["status"]

    if validated["status"] != "success":
        can_continue = False
        log_data["error"] = validated["error"]

        
    trace_data(
        request_id=request_id,
        step_name="input_validation",
        step_order=step,
        status=validated["status"],
        error=validated["error"]
        )
    
    
    

    

    if can_continue:
        
        step += 1
        cleaned_input = validated["result"]
        log_data["cleaned_input"] = cleaned_input

        api_attempts = 0
        
        while api_attempts < 3:
            api_attempts += 1
            loop_status = "retry_exhausted"
            loop_errors = {"error_503", "time_out","connection_error"}
            called_api = call_api(cleaned_input)
       
            if called_api["status"] != "success":
                if called_api["error"] in loop_errors:
                    continue
                else:
                    loop_status = "non_retryable"
                    break
                 
            else:
                loop_status = "success"
                break
        
        log_data["attempts"] = api_attempts
        log_data["status"] = called_api["status"]

        if loop_status == "non_retryable" or loop_status == "retry_exhausted":
            can_continue = False
            log_data["error"] = called_api["error"]
            
    
        trace_data(
            request_id=request_id,
            step_name="api_call",
            step_order=step,
            status=called_api["status"],
            error=called_api["error"]
            )


    if can_continue:
        step += 1
        raw_response = called_api["result"]
        log_data["raw_response"] = raw_response

        filtered_data = filter_data(raw_response,id)
        log_data["status"] = filtered_data["status"]



        if filtered_data["status"] != "success":
            can_continue = False
            log_data["error"] = filtered_data["error"]            
            
        trace_data(
            request_id=request_id,
            step_name="output_filtration",
            step_order=step,
            status=filtered_data["status"],
            error=filtered_data["error"]
            )

    if can_continue:
        step += 1
        log_data["post_id"] = filtered_data["result"]["id"]
        log_data["title"] = filtered_data["result"]["title"]
    
    ai_attempts = 0
    while ai_attempts < 3:
        
        loop_status = "success"
        ai_attempts += 1
        loop_errors = {"status_code_error", "time_out", "connection_error"}
        ai_called = ai_call(f"status: {log_data["status"]} ,error: {log_data["error"]}")
        if ai_called["status"] == "success":            
            break
        elif ai_called["error"] in loop_errors:
            loop_status = "retry_exhausted"
            continue
        else:
            loop_status = "non_retryable"
            break
    if loop_status != "success":
            can_continue =False
            log_data["ai_generated"] = "false"
            log_data["ai_explanation"] = ai_called["status"]
            
    
    if can_continue:
        parsed_json = parse_json(ai_called["result"])
        if parsed_json["status"] != "success":
            can_continue = False
            log_data["ai_generated"] = "false"

    
    if can_continue:
        validate_parsed_json = validate_ai_response(parsed_json["result"])
        if validate_parsed_json["status"] != "success":
            can_continue = False
            log_data["ai_generated"] = "false"
    if can_continue:
        log_data["ai_generated"] = "true"
        log_data["ai_explanation"] = ai_called["result"]

    
            
        
    
    save = save_log(log_data)
    step += 1

    if save["status"] != "success":
        
        trace_data(
            request_id=request_id,
            step_name="save_log",
            step_order=step,
            status=save["status"],
            error=save["error"]
            ) 
        return save
        
    trace_data(
            request_id=request_id,
            step_name="save_log",
            step_order=step,
            status=save["status"],
            error=save["error"]
            ) 
    
    return log_data


    


    
    

result = main()
print(result)


