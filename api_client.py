import requests
import time

from utils import status_check,clean_post,filter_post,display_post

from utils import status_check
class APIClient:
    def __init__(self,base_url,header):
        self.base_url = base_url
        self.header = header
    def build_url(self, endpoint):
        return self.base_url + endpoint
         
    def request(self,endpoint,params=None,json=None,method=None):
        attempts = 0
        url = self.build_url(endpoint)
        while attempts < 3:
            try:
                if method == "get":
                    response = requests.get(url,params=params,timeout=2)
                elif method == "post":
                    response = requests.post(url,headers=self.header,json=json,timeout=2)
                data =status_check(response)
                if isinstance(data,str):
                    print(f"{data} Retry...")
                else:
                    return data
            except requests.exceptions.Timeout:
                print( "Time Out Error. Retry...")
            except requests.exceptions.RequestException as e:
                print( f"API Failled  {e} Retry...")
            attempts += 1
        return {
            "Error": "Failled After Retry",
        }
            