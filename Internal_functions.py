import json
#------------------------- Internal responses me status me success or failed hoga ----------------
def build_internal_response(status,result=None,error=None):
    return {
        "status": status,
        "result": result,
        "error": error
    }

def json_parse(data):
    try:
        json_data = json.loads(data)
        return build_internal_response(
            status="success",
            result=json_data,
            error=None
        )
    except:
        return build_internal_response(
            status="failed",
            result=None,
            error="json_parsing_fail"
        )

def validate_ai_response(data):
    json_data = json_parse(data)
    if json_data["status"] == "success":
        json_data = dict(json_data)
        if "explanation" in json_data["result"]:
            return build_internal_response(
                status="success",
                result=json_data["result"]["explanation"],
                error=None,
        )
        else:
            return build_internal_response(
                status="failed",
                result=None,
                error="explanation_key_not_exist"
            )
    return build_internal_response(
            status="failed",
            result=None,
            error="data_not_json",  
            )
    
