import requests 
import json
from utils import build_response

def ai_call(message):
    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers= {
            "Authorization": "Bearer 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",
            "Accept": "application/json"
            },
            data=json.dumps({
                "model": "baidu/cobuddy:free",
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
                user_input=None,
                result=response.json()['choices'][0]['message']['content'],
                error=None
            )
        else:
            return build_response(
                status="ai_call_failed",
                user_input=None,
                result=None,
                error=f"status_code_error {response.status_code}"
            )
    except requests.exceptions.Timeout:
        return build_response(
            status="ai_call_failed",
            user_input=None,
            result=None,
            error="time_out"
        )
    except requests.exceptions.ConnectionError:
        return build_response(
            status="ai_call_failed",
            user_input=None,
            result=None,
            error="connection_error"
        )
    except requests.exceptions.RequestException as e:
        return build_response(
            status="ai_call_failed",
            user_input=None,
            result=None,
            error= str(e)
        )

