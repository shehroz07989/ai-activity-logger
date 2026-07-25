from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import ai_activity_logger

app = FastAPI(title="AI Activity Logger API")

# Input ka structure
class LogRequest(BaseModel):
    user_input: int | str

@app.get("/")
def read_root():
    return {"message": "AI Activity Logger is Live! Use /log endpoint to track AI calls."}

@app.post("/log")
def create_log(request: LogRequest):
    try:
        # Tumhara existing function yahan call hoga
        result = ai_activity_logger.ai_activity_logger(request.user_input)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
