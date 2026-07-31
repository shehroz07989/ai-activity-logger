import schedule 
import time
from main import run

def scheduler():
    try:
        print("scheduler is running")
        run(33)
    except Exception as e:
        print(f"Runtime Error: {str(e)}")
schedule.every(1).hours.do(scheduler)
print("scheduler waiting")

while True:
    schedule.run_pending()
    time.sleep(1)
