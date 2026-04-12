# Example: Working with APIs
import requests

response = requests.get("https://api.github.com")
if response.status_code == 200:
    print("API call successful")
    print(response.json())
