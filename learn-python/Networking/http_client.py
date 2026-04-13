"""
HTTP client examples using urllib (standard library).
"""
from urllib.request import urlopen, Request
from urllib.parse import urlencode, urlparse, parse_qs
from urllib.error import URLError, HTTPError
import json

# URL parsing
url = "https://api.example.com/search?q=python&page=2&sort=relevance"
parsed = urlparse(url)
print("URL Parsing:")
print(f"  Scheme: {parsed.scheme}")
print(f"  Host: {parsed.netloc}")
print(f"  Path: {parsed.path}")
print(f"  Query: {parsed.query}")
print(f"  Params: {parse_qs(parsed.query)}")

# Building URLs
params = urlencode({"q": "python tutorial", "limit": 10, "offset": 0})
print(f"\nEncoded params: {params}")

# GET request
def get_request(url):
    try:
        req = Request(url, headers={"User-Agent": "Python-Example/1.0"})
        with urlopen(req, timeout=5) as response:
            data = response.read().decode()
            print(f"Status: {response.status}")
            print(f"Headers: {dict(response.headers)}")
            return data
    except HTTPError as e:
        print(f"HTTP Error: {e.code} {e.reason}")
    except URLError as e:
        print(f"URL Error: {e.reason}")
    return None

# POST request
def post_request(url, data):
    payload = json.dumps(data).encode('utf-8')
    req = Request(url, data=payload, method='POST')
    req.add_header('Content-Type', 'application/json')
    try:
        with urlopen(req, timeout=5) as response:
            return json.loads(response.read().decode())
    except (HTTPError, URLError) as e:
        print(f"Error: {e}")
    return None

# Download file
def download_file(url, filename):
    try:
        req = Request(url, headers={"User-Agent": "Python-Example/1.0"})
        with urlopen(req, timeout=10) as response:
            total = int(response.headers.get('Content-Length', 0))
            downloaded = 0
            with open(filename, 'wb') as f:
                while True:
                    chunk = response.read(8192)
                    if not chunk:
                        break
                    f.write(chunk)
                    downloaded += len(chunk)
            print(f"Downloaded {downloaded} bytes to {filename}")
    except (HTTPError, URLError) as e:
        print(f"Download error: {e}")

if __name__ == "__main__":
    print("\n--- GET Request ---")
    try:
        result = get_request("https://httpbin.org/get")
        if result:
            print(f"Response (first 200 chars): {result[:200]}")
    except Exception:
        print("Could not connect (no internet)")

    print("\n--- POST Request ---")
    try:
        result = post_request(
            "https://httpbin.org/post",
            {"name": "Alice", "msg": "Hello"}
        )
        if result:
            print(f"Response: {json.dumps(result, indent=2)[:200]}")
    except Exception:
        print("Could not connect (no internet)")
