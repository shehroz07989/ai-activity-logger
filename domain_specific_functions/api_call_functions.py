from general_functions.utils import build_response
import requests
def filter_api_data(data):
    if "id" in data and "title" in data:
        filtered_data= {
            "id": data.get("id"),
            "title": data.get("title")
        }
    else:
        return build_response(
        status = "filtration_failed",
        result = None,
        error = "id or title dose not exist"
        )
    return build_response(
        status = "success",
        result = filtered_data,
        error = None  
    )
def call_api(data):
   
    try:
        response = requests.get(f"https://jsonplaceholder.typicode.com/posts/{data}", timeout=2)
        if response.ok:
            try:
                cleaned_response = response.json()
                return build_response(
                        status = "success",
                        user_input = data,
                        result = cleaned_response,
                        error = {
                            "name": "invalid_json_error",
                            "type": "temporary",
                            "detail": "ValueError"
                            }
                            )
            except ValueError:
                return build_response(
                    status = "api_failed",
                    user_input = data,
                    result = None,
                    error = {
                    "name": "invalid_json_error",
                    "type": "temporary",
                    "detail": "ValueError"
                    }
                    )
        else:
            return build_response(
                 status="api_failed",
                 user_input=data,
                 error={
                     "name": "status_code_error" ,
                     "type": "temporary",
                     "detail": response.status_code
                 }
            )
    except requests.exceptions.Timeout:
        return build_response(
                 status="api_failed",
                 user_input=data,
                 error={
                     "name": "time_out_error",
                     "type": "temporary",
                     "detail": "time_out"
                 }
            )
    except requests.exceptions.ConnectionError:
        return build_response(
                 status="api_failed",
                 user_input=data,
                 error={
                    "name": "connection_error",
                    "type": "temporary",
                    "detail": "connection_error"
                 }
            )
    except requests.exceptions.RequestException as e:
        return build_response(
                 status="api_failed",
                 user_input=data,
                 error={
                     "name": "request_exception_error",
                     "type": "permanent",
                     "detail": str(e)
                 }
            )
   


   

    
def api_call_response_decision(data):
    errors = {503,"connection_error","time_out"}
    if data["error"] in errors:
        return build_response(
            status="success",
        )
    else:
        return build_response(
            status="failed"
        )
    