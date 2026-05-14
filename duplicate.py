from Internal_functions import build_internal_response, validate_ai_response
import requests
import json
from utils import build_response

def ai_call():
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
                    "model": "nvidia/nemotron-3-nano-30b-a3b:free",
                    "messages": [
                        {
                            "role": "system",
                            "content": "me 1 system bna rha ho jisme tumhara role ha error ya result explain krne ke maslan agr error milta ha tumhe ke input must be integer tumne english me likhna ha error aya qke user ne input me integer nhi dala ya string dali or tumhe strictly kha jata ha ke tumne sirf json return krna ha jo explanation kro ge tum usse 1 hi line me json me explanation key ke andr rakhna ha 1 hi or usi me explanation yhi tumhara kaam ha iske ilawa forbiden ha tumhare lia kuch bi krna "
                        },
                        {
                               "role": "user",
                                 "content": "status: filtration_failled,error  required filed dose not exist"
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
                data.update({
                    "status": "ai_call_failed",
                    "error":  f"status_code_error {response.status_code}",
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
            status="hro",
            user_input=None,
            result=None,
            error=data["error"]
            )
    
        



print(ai_call())