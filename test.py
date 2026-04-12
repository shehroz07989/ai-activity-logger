import requests
from api_client import  filter_fetch, request

class task_10:
    def __init__(self,url):
        self.url = url

    def start_system(self):
        data = request(self.url)
        #first Waya: if isinstance(data,str):
            #return data
        #dosra way: api_client ke funcion ke andr 
        if "Error" in data:
            return data

        
        cleaner = filter_fetch(data)
        print(cleaner)

        
        
api = task_10("https://jsonplaceholder.typicode.com/po1sts")
result = api.start_system()
print (result)

