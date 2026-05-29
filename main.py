import uuid

from services.main_executor import main_executor
from general_functions.utils import terminate_flow
from services.trace_service import trace_steps

def main():
        
        id = input("Enter id: ")
        request_id = str(uuid.uuid4())
        log_data = {
                    "input": id,
                    "cleaned_input": None,
                    "status": None,
                    "post_id": None,
                    "error": None,       
                    "title": None,
                    "raw_response": None,
                    "attempts" : None,
                    "request_id": request_id,
                    "ai_generated": None,
                    "ai_explanation": None
                }
        
        
        step = 1
        trace_steps(request_id=request_id,step_name="input_validation",step_order=step)
        validated = main_executor(input=id,function_name="validate")
        trace_steps(standard_response=validated,request_id=request_id,step_name="input_validation",step_order=step)
        log_data["status"] = validated["status"]
        if validated["status"] != "success":
                log_data["error"] = validated["error"]
                return terminate_flow(log_data)
        


        log_data["cleaned_input"] = validated["result"]
        step += 1
        trace_steps(request_id=request_id,step_name="api_call",step_order=step)
        called_api_workflow = main_executor(function_name="api_call_workflow",input=log_data["cleaned_input"])
        trace_steps(standard_response=called_api_workflow,request_id=request_id,step_name="api_call",step_order=step)
        log_data["status"] = called_api_workflow["status"]
        if called_api_workflow["status"] != "success":
                log_data["error"] = called_api_workflow["error"]
                log_data["attempts"] = called_api_workflow["result"]["attempts"]
                return terminate_flow(log_data)
        


        log_data["raw_response"] = called_api_workflow["result"]["response"]
        log_data["attempts"] = called_api_workflow["result"]["attempts"]
        step += 1

        trace_steps(request_id=request_id,step_name="api_response_filtration",step_order=step)
        filtered_data = main_executor(function_name="filter_data",input=log_data["raw_response"])
        trace_steps(standard_response=filtered_data,request_id=request_id,step_name="api_response_filtration",step_order=step)

        log_data["status"] = filtered_data["status"]
        if filtered_data["status"] != "success":
                log_data["error"] = filtered_data["error"]
                return terminate_flow(log_data)
        


        
        log_data["post_id"] = filtered_data["result"]["id"]
        log_data["title"] = filtered_data["result"]["title"]
        step += 1

        trace_steps(request_id=request_id,step_name="ai_call_workflow",step_order=step)
        ai_called_workflow = main_executor(function_name="ai_call_proccess",input=f"status: {log_data["status"]} error: {log_data["error"]}")
        trace_steps(standard_response=ai_called_workflow,request_id=request_id,step_name="ai_call_workflow",step_order=step)
        log_data["status"] = ai_called_workflow["status"]
        if ai_called_workflow["status"] != "success":
                log_data["error"] = ai_called_workflow["error"]
                log_data["ai_generated"] = "false"
                return terminate_flow(log_data)
        



        log_data["ai_generated"] = "true"
        log_data["ai_explanation"] = ai_called_workflow["result"]

        step += 1

        trace_steps(request_id=request_id,step_name="save_log",step_order=step)
        saved_log = main_executor(function_name="save_log",input=log_data)
        if saved_log["status"] != "success":
                trace_steps(standard_response=saved_log,request_id=request_id,step_name="save_log",step_order=step)
                return saved_log
        
        trace_steps(standard_response=saved_log,request_id=request_id,step_name="save_log",step_order=step)
        return log_data

print(main())