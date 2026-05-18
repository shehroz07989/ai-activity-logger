import json
#------------------------- Internal responses me status me success or failed hoga ----------------
def build_specific_response(status,result=None,error=None,error_type=None,error_detail=None,status_code=None):
    return {
        "status": status,
        "result": result,
        "error_type": error_type,
        "error": error,
        "status_code": status_code
    }
