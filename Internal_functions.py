import json
#------------------------- Internal responses me status me success or failed hoga ----------------
def build_internal_response(status,result=None,error=None):
    return {
        "status": status,
        "result": result,
        "error": error
    }
