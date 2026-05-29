from general_functions.utils import validate,save_log,build_response
from work_flows.ai_workflow import ai_call_proccess
from domain_specific_functions.api_call_functions import filter_api_data
from work_flows.api_call_workflow import api_call_workflow



def main_executor(function_name,input):
    function_list = {
        "validate": validate,
        "api_call_workflow": api_call_workflow,
        "filter_data": filter_api_data,
        "save_log": save_log,
        "ai_call_proccess": ai_call_proccess
    }

    function_to_execute = function_list.get(function_name)
    
    if not function_to_execute:
        return build_response(
            status="failed",
            user_input=input,
            error=f"function_dose_not_exist {function_name}"
        )
    
    
    return function_to_execute(input)
   


