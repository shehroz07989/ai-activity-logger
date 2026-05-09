import requests
import sqlite3
import json
from fastapi import HTTPException
def build_response(status,user_input,result,error):
    return {
        "status": status,
        "input": user_input,
        "result": result,
        "error": error,
    }
def validate(data):
    try:
        cleaned_data = int(data)
    except ValueError:
        return build_response(
                status="validation_failed",
                user_input=data,
                result=None,
                error="input must be integer"
                )
    
    if cleaned_data < 1 or cleaned_data > 100:
        return build_response(
            status="validation_failed",
            user_input=data,
            result=None,
            error="input must be between 1-100"
            )
    
    
    return build_response(
                        status = "success",
                        user_input = data, 
                        result = cleaned_data,
                        error = None
                         )

    
def call_api(data):
   
    try:
        response = requests.get(f"https://jsonplaceholder.typicode.com/posts/{data}", timeout=2)
        if 199 < response.status_code < 300:
            try:
                cleaned_response = response.json()
                return build_response(
                        status = "success",
                        user_input = data, 
                        result = cleaned_response,
                        error = None
                         )
            except ValueError:
                return build_response(
                            status = "api_failed",
                            user_input = data, 
                            result = None,
                            error = "invalid json"
                            )
        elif response.status_code == 503:
            return build_response(
                            status = "api_failed",
                            user_input = data, 
                            result = None,
                            error = "error_503"
                            )
        else:
            return build_response(
                            status = "api_failed",
                            user_input = data, 
                            result = None,
                            error = f"status code error {response.status_code}"
                            )


    except requests.exceptions.Timeout:
        return build_response(
        status = "api_failed",
        user_input = data, 
        result = None,
        error = "time_out"
           )
    except requests.exceptions.ConnectionError:
        return build_response(
        status = "api_failed",
        user_input = data, 
        result = None,
        error = "connection_error"
        )
    except requests.RequestException:
        return build_response(
        status = "api_failed",
        user_input = data, 
        result = None,
        error = "request_failed"
        )
    


def filter_data(data,user_input):
    if "id" in data and "title" in data:
        filtered_data= {
            "id": data.get("id"),
            "title": data.get("title")
        }
    else:
        return build_response(
        status = "filtration_failed",
        user_input = user_input, 
        result = None,
        error = "id or title dose not exist"
        )
    return build_response(
        status = "success",
        user_input = user_input, 
        result = filtered_data,
        error = None  
    )

def save_log(data):
    allowed_values = ["validation_failed", "api_failed", "filtration_failed", "success"]
    
    if data["status"] in allowed_values:
        
        try:
            conn = sqlite3.connect("system.db")
            save = """
                INSERT INTO logs (status, input, cleaned_input, error, post_id, title, raw_response,attempts)
                VALUES( ?, ?, ?, ?, ?, ?, ?,?)
                
                    """
            if isinstance (data["raw_response"],dict):
                data["raw_response"] = json.dumps(data["raw_response"])
            elif isinstance (data["raw_response"],str):
                pass
            elif isinstance  (data["raw_response"],type(None)):
                pass
            else:
                data["raw_response"] = str(data["raw_response"])
                
            
            cursor = conn.cursor()
            cursor.execute(save,(data["status"], data["input"], data["cleaned_input"], data["error"], data["post_id"], data["title"], data["raw_response"],data["attempts"]))
            conn.commit()
            
            return build_response(
                status = "success",
                user_input = data["input"], 
                result = data,
                error = None
                    )
        except Exception as e:
            return build_response(
                status = "db_failed",
                user_input = data["input"], 
                result = None,
                error = str(e), 
                    )
        finally:
            conn.close()
    else:
         return build_response(
                status = "status_failed",
                user_input = data["input"], 
                result = None,
                error = "allowed values dose not exist in status"
                    )
    
   