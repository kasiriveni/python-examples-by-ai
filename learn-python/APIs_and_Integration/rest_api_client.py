"""
Example of a REST API client using the requests library.
"""
import requests

def get_user_data(user_id):
    url = f"https://jsonplaceholder.typicode.com/users/{user_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

if __name__ == "__main__":
    user_data = get_user_data(1)
    print(user_data)
