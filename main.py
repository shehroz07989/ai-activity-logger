from api_client import APIClient
from utils import status_check,clean_post,filter_post,display_post
from dotenv import load_dotenv
import os
load_dotenv()
header = os.getenv("API_KEY")
api = APIClient(
    base_url="https://reqres.in",
    header={"x-api-key": header,}
)



result = api.request(endpoint="/api/login",method="post", json={"email": "eve.holt@reqres.in", "password": "cityslicka"})
print(result)