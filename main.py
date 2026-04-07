from api import retry_request
from utils import json_return, filter_posts, display_posts
def main():
    url = "https://jsonplaceholder.typicode.com/posts"
    params =  {"userId": 1}

    response = retry_request(url,params)
    if not response:
        print("API Failled")
        return
    
    data = json_return(response)
    filter_ = filter_posts(data)
    display_posts(filter_)
    
    
    


main()