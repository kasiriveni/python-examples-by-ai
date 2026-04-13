"""
Example of using the requests library to send POST requests.
"""
import requests

def create_user(name, job):
    url = "https://reqres.in/api/users"
    payload = {"name": name, "job": job}
    response = requests.post(url, json=payload)
    return response.json()

if __name__ == "__main__":
    user = create_user("John Doe", "Developer")
    print(user)
