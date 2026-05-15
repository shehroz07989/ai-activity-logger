import requests
import sqlite3
import time
import json
from fastapi import HTTPException
from Internal_functions import build_internal_response, validate_ai_response
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
                            error = "invalid_json"
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
                INSERT INTO logs (status, input, cleaned_input, error, post_id, title, raw_response,attempts,request_id,ai_generated,ai_explanation)
                VALUES( ?, ?, ?, ?, ?, ?, ?,?,?,?,?)
                
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
            cursor.execute(save,(data["status"], data["input"], data["cleaned_input"], data["error"], data["post_id"], data["title"], data["raw_response"],data["attempts"],data["request_id"],data["ai_generated"],data["ai_explanation"]))
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
    

def trace_loger(trace_data):
    conn = sqlite3.connect("system.db")
    cursor = conn.cursor()
    cursor.execute("""
                    INSERT INTO trace (request_id,step_name,step_order,status,error) 
                    VALUES (:request_id,:step_name,:step_order,:status,:error)
                        """,trace_data) 
    conn.commit()
    conn.close()


def trace_data(
        request_id,
        step_name,
        step_order,
        status,
        error = None
        ):
    data = {
        "request_id": request_id,
        "step_name": step_name,
        "step_order": step_order,
        "status": status,
        "error": error
    }
    trace_loger(data)

def ai_call(message):
    attempts = 0
    while attempts < 3:
        attempts += 1
        status = True        
        data = {
            "status":None,
            "result": None,
            "error": None
        }
        try:
            
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Accept": "application/json",
                    "Authorization": "Bearer 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"
                },
                data=json.dumps(
                    {
                    "model": "openai/gpt-oss-120b:free",
                    "messages": [
                        {
                            "role": "system",
                            "content": "me 1 system bna rha ho jisme tumhara role ha error ya result explain krne ke maslan agr error milta ha tumhe ke input must be integer tumne english me likhna ha error aya qke user ne input me integer nhi dala ya string dali or tumhe strictly kha jata ha ke tumne sirf json return krna ha jo explanation kro ge tum usse 1 hi line me json me explanation key ke andr rakhna ha 1 hi or usi me explanation yhi tumhara kaam ha iske ilawa forbiden ha tumhare lia kuch bi krna agr status success hua to kehana ha ke user ne shi input dia pora workflow shi chala isse ache andaaz me likhna ha  "
                        },
                        {
                               "role": "user",
                                 "content": message,
                            }
                        ]
                    }
                ),
                timeout=60,
                )
            
            if  response.ok:
                
                json_parsing = validate_ai_response(response.json()['choices'][0]['message']['content'])
                if json_parsing["status"] == "success":
                    data.update({
                        "status": json_parsing["status"],
                        "result": json_parsing["result"],
                        "error": json_parsing["error"]
                                })
                    break
                else:
                    status = False
                    data.update({
                          "status": json_parsing["status"],
                          "error": json_parsing["error"]
                    })
                    continue
            else:
                status = False
                data.update({
                    "status": "ai_call_failed",
                    "error":  f"status_code_error {response.status_code} ",
                })
                continue
        except requests.exceptions.Timeout:
            status = False
            data.update({
                "status": "ai_call_failed",
                "error": "time_out"
            })
            continue
        except requests.ConnectionError:
            status = False
            data.update({
                "status": "ai_call_failed",
                "error": "connection_error"
            })
            continue

        except requests.exceptions.RequestException as e:
            status = False
            data.update({
                "status": "ai_call_failed",
                "error": str(e)
            })
            continue
    

    if status == True:
        return build_response(
            status=data["status"],
            user_input=None,
            result=data["result"],
            error=None
        )
    else:
        return build_response(
            status=data["status"],
            user_input=None,
            result=None,
            error=data["error"]
            )
    

