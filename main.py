from utils import validate, call_api,filter_data,save_log

def main():
   
    id = input("Enter id: ")
    log_data = {
                "input": id,
                "cleaned_input": None,
                "status": None,
                "post_id": None,
                "error": None,
                "title": None,
                "raw_response": None,
                "attempts" : None
            }
   
    #------------------------------- Validation Block --------------------------------------------
   
    validated = validate(id)
    log_data["status"] = validated["status"]
    if validated["status"] != "success":
        log_data["error"] = validated["error"]
        save_db = save_log(log_data)
        if save_db["status"] != "success":
            return save_db
        else:
            return log_data
   

    cleaned_input = validated["result"]
    log_data["cleaned_input"] = cleaned_input

    #----------------------------------- API Block + Loop -----------------------------------------------
    attempts = 0
    loop_status = "retry_exhausted"
    while attempts < 3:
            attempts += 1
            errors = ["error_503", "time_out","connection_error"]
            called_api = call_api(cleaned_input)
       
            if called_api["status"] != "success":
                if called_api["error"] in errors:
                    continue
                else:
                    loop_status = "non_retryable"
                    break
                 
            else:
                loop_status = "success"
                break

    #----------------------------- Decision Block (Loop) -------------------------------------------
 
    if loop_status == "non_retryable" or loop_status == "retry_exhausted":
        log_data["status"] = called_api["status"]
        log_data["error"] = called_api["error"]
        log_data["attempts"] = attempts
        save_db = save_log(log_data)
        if save_db["status"] != "success":
            return save_db
        else:
            return log_data
    else:
        log_data["attempts"] = attempts
        log_data["status"] = called_api["status"]
        raw_response = called_api["result"]
        log_data["raw_response"] = raw_response

    #------------------------------------- Filtration Block ----------------------------------------------------
    filtered_data = filter_data(raw_response,id)
    log_data["status"] = filtered_data["status"]
    if filtered_data["status"] != "success":
        log_data["error"] = filtered_data["error"]
        save_db = save_log(log_data)
        if save_db["status"] != "success":
            return save_db
        else:
            return log_data
    # ---------------------------------- Success Block ---------------------------------
    log_data["post_id"] = filtered_data["result"]["id"]
    log_data["title"] = filtered_data["result"]["title"]
    save_db = save_log(log_data)
    if save_db["status"] != "success":
        return save_db
    else:
        return log_data
result = main()
print(result)


