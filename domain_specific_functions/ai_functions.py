from general_functions.utils import build_response
import requests
from dotenv import load_dotenv
import os
import json
load_dotenv("secure_files/.env")
api_key = os.getenv("OPENROUTER_KEY")
def validate_ai_response(data):
    try:
        json_data = dict(data)
        if "explanation" in json_data:
            return build_response(
                status="success",
                user_input=None,
                result=json_data["explanation"],
                error=None,
                )
    except TypeError:
        return build_response(
                status="failed",
                user_input=None,
                result=None,
                error="explanation_key_not_exist"
            )
   
    

def ai_call(message):
    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers= {
            "Authorization":f"Bearer {api_key}" ,
            "Accept": "application/json"
            },
            data=json.dumps({
                "model": "openai/gpt-oss-120b:free",
                "messages": [
                    {
                        "role": "system",
                        "content": """You are a JSON-only explanation bot. INPUT: You receive status (success/failed) and error (text or None). RULES: Return ONLY a single-line JSON with one key "explanation". No markdown, no extra text, no line breaks inside JSON. WHAT TO WRITE: If status is "success", say user gave correct input and workflow ran perfectly. If status is "failed", read the error and explain simply in English why it happened (e.g., "input must be integer" means user entered string instead of integer). EXAMPLES: For success → {"explanation":"User provided correct input and workflow completed successfully."} For failed with error "input must be integer" → {"explanation":"Error: user entered a string instead of an integer value."}"""
                    },
                    {
                        "role": "user",
                        "content": message,
                    }
                ]
            }),
            timeout=60
        )
        if response.ok:
            return build_response(
                status="success",
                result=response.json()['choices'][0]['message']['content'],
                error={
                            "name": None,
                            "type": None,
                            "detail": None
                            }
            )
        else:
            return build_response(
                status="ai_call_failed",
                result=None,
                error={
                    "name": "status_code_error",
                    "type":"temporary",
                    "detail": f"status_code_error_{response.status_code}"
                }
            )
    except requests.exceptions.Timeout:
        return build_response(
            status="ai_call_failed",
            error={
                     "name": "time_out_error",
                     "type": "temporary",
                     "detail": "requests.exceptions.Timeout_error"
                 }
        )
    except requests.exceptions.ConnectionError:
        return build_response(
            status="ai_call_failed",
            error={
                    "name": "connection_error",
                    "type": "temporary",
                    "detail": "requests.exceptions.ConnectionError"
                 }
        )
    except requests.exceptions.RequestException as e:
        return build_response(
            status="ai_call_failed",
            error= {
                     "name": "request_exception_error",
                     "type": "permanent",
                     "detail": str(e)
                 }
        )

