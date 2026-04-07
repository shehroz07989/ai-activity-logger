import time
import requests
def retry_request(url,params):
    for i in range(3):
        
        try:
            response = requests.get(url,params=params,timeout= 5)
            if response.status_code == 200:
                print("Success Request")
                return response
            else:
                print(f"Status code Error: {response.status_code} Retrying  {i+1}")
        except requests.exceptions.Timeout:
            print(f"Time out error Retrying  {i+1}")
        except requests.exceptions.RequestException:
            print(f"API Error Retrying  {i+1}")
        time.sleep(2)