from test_single import URL
import requests
from dotenv import load_dotenv
import os
load_dotenv()
headers = {"accept": "application/json", "authorization": os.getenv('RUNPOD_API_KEY')}
response = requests.get(os.path.join(URL, 'health'),  headers=headers)

print(response.json())