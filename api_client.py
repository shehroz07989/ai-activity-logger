from fastapi import FastAPI, HTTPException
import sqlite3
from data_base import get_all_logs,get_log_by_id
from utils import validate


app = FastAPI()
@app.get("/logs")
def main_endpoint():
    return get_all_logs()
    
@app.get("/logs/{user_id}")
def get_by_id(user_id:int):
    response =  get_log_by_id(user_id)
    if response == "error_in_db" :
        raise HTTPException(status_code=500,detail={
            "response": None,
            "error": "error_in_db",
        })
    elif response == "validation_failed":
        raise HTTPException(status_code=400,detail={
            "response": None,
            "error": "Input must be between 1-100",
        })
    elif response is None:
        raise HTTPException(status_code=404,detail={
            "response": None,
            "error": "not_found",
        })
    return {
        "response": response,
        "error": None,
    }