from general_functions.utils import build_response
def retry_policy(error):
    if error["type"] == "temporary":
        return build_response(
            status="success",
            result= {
                "action": "retry",
                "payload":{
                    "max_attempts": 3
                    }
                }
            )
    if error["type"] == "permanent":
        return build_response(
            status="success",
            result={
                "action": "terminate",
                "payload": None
            }
        )
   
