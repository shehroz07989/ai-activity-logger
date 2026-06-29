import schedule 
import time
from ai_activity_logger import ai_activity_logger

def scheduler():
    try:
        print("scheduler is running")
        ai_activity_logger(33)
    except Exception as e:
        print(f"Runtime Error: {str(e)}")
schedule.every(1).hours.do(scheduler)
print("scheduler waiting")

while True:
    schedule.run_pending()
    time.sleep(1)
