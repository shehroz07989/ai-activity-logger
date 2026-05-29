import time
from domain_specific_functions.api_call_functions import call_api,api_call_response_decision

def api_call_workflow(data):
    attempts = 0
    while attempts < 3:
        attempts += 1
        called_api = call_api(data)
        if called_api["status"] != "success":
            decision = api_call_response_decision(called_api)
            if decision["status"] == "success":
                time.sleep(2** attempts)
                continue
            else:
                called_api["result"] = {
                    "response": called_api["result"],
                    "attempts": attempts
                }
                return called_api
        break
    called_api["result"] = {
                    "response": called_api["result"],
                    "attempts": attempts
                }
    return called_api


    



