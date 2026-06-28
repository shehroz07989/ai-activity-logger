from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI,HTTPException

from services.sqlite_query_execution_service import sqlite_execution_service
#In sqlite Fetched Data Always Return in Dictionary because of consistent contract
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/metrics")
def metrics():
    summary = sqlite_execution_service(query="""
           SELECT
                    COUNT(*) AS total_calls,
                    COUNT(CASE WHEN status = 'success' THEN 1 END) AS success_requests,
                    COUNT(CASE WHEN status != 'success' THEN 1 END) AS fail_requests,
                    COUNT(CASE WHEN ai_generated = 'true' THEN 1 END) AS ai_success_requests,
                    COUNT(CASE WHEN ai_generated != 'true' THEN 1 END) AS ai_fail_requests,
                    COUNT(CASE WHEN ai_generated = 'true' THEN 1 END) * 100.0 /NULLIF( COUNT(*),0) AS ai_success_rate ,
                    COUNT(CASE WHEN ai_generated != 'true' THEN 1 END) * 100.0 / NULLIF(COUNT(*),0) AS ai_failure_rate,
                    COUNT(CASE WHEN status = 'success' THEN 1 END ) * 100.0 / NULLIF(COUNT(*),0) AS success_rate,
                    COUNT(CASE WHEN status != 'success' THEN 1 END ) * 100.0 / NULLIF(COUNT(*),0) AS failure_rate
                    FROM logs
                    """,fetch_mode="one")
    


    
    status_breakdown = sqlite_execution_service(query="""
            SELECT
                status, COUNT(*) AS total
                FROM logs
                GROUP BY status
                ORDER BY total DESC
                        """,fetch_mode="all")
    if summary["status"] != "success" and status_breakdown["status"] != "success":
        raise HTTPException(status_code=500,detail={
            "error": "something_went_wrong"
        })
    visible_summary = summary["result"]
    visible_status_breakdown = status_breakdown["result"]

    
    
    return {
            "summary":visible_summary,
            "status_breakdown": visible_status_breakdown,
            }
