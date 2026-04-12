# APIs & Integration: simple API client using requests
# Requires `requests` package
import requests

resp = requests.get('https://jsonplaceholder.typicode.com/todos/1')
if resp.status_code == 200:
    print(resp.json())
else:
    print('error', resp.status_code)
