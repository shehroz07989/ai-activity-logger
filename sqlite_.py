from fastapi import FastAPI
from general_functions.utils import build_response
import sqlite3
app = FastAPI()
@app.get("/metrics")
def get_metrics():
    conn = sqlite3.connect("sqlite/system.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    query = """
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
                    """
    cursor.execute(query)
    summmary = dict(cursor.fetchone())
    


    group_query = """
            SELECT
                status, COUNT(*) AS total
                FROM logs
                GROUP BY status
                ORDER BY total DESC
                        """
    cursor.execute(group_query)
    status = cursor.fetchall()
    x = []
    for i in status:
        x.append((dict(i)))
    
    conn.close()
    return {
        "summary": summmary,
        "status_breakdown": x
    }


def query_execute_fetchone(query,):
    conn = None
    conn = sqlite3.connect("sqlite/system.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetch() 
    conn.close()
    return result
    
def query_execute(query,fetch_mode):
    try:
        conn = sqlite3.connect("sqlite/system.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(query)
        if fetch_mode == "all":
            fetched_data = cursor.fetchall()
            result = []
            for i in fetched_data:
                result.append(dict(i))
            return build_response(
                status="success",
                result=result
                )
        if fetch_mode == "one":
            result = cursor.fetchone() 
            return build_response(
                status="success",
                result=dict(result)
            )
        else:
            return build_response(
                status="query_failed",
                user_input={
                    "query": query,
                    "fetch_mode": fetch_mode
                },
                error="fetch_mode_is_only_one_or_all"
            )

    except sqlite3.ProgrammingError as e:
        return build_response(
            status="query_failed",
            user_input={
                    "query": query,
                    "fetch_mode": fetch_mode
                },
            error=str(e)
        ) 
    except sqlite3.OperationalError as e:
        return build_response(
            status="query_failed",
            user_input={
                    "query": query,
                    "fetch_mode": fetch_mode
                },
            error=str(e)
        ) 
    except sqlite3.Error as e:
        return build_response(
            status="query_failed",
            user_input={
                    "query": query,
                    "fetch_mode": fetch_mode
                },
            error=str(e)
        ) 
    finally:
        if conn != None:
            conn.close()


print(query_execute(query="""
            SELECt
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
                    """,fetch_mode="one"))