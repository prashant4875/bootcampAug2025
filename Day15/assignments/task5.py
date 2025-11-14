import requests
import json 
from datetime import datetime

# response = requests.get("https://jsonplaceholder.typicode.com/posts/1")

# data = response.json()
# print(data['title'])
# print(data['body'][:50])

# params = {
#     'userId': 1,
#     '_limit': 6
# }

# print(f"Requesting posts with parameters: {params}")
# response = requests.get(
#     "https://jsonplaceholder.typicode.com/posts",
#     params=params
# )

# print(response.json())

# 1. Make a GET request to https://api.github.com/users/YOUR_USERNAME and print your profile info

username = "prashant4875"  # Replace with your GitHub username
response = requests.get(f"https://api.github.com/users/{username}")

profile_data = response.json()
print(json.dumps(profile_data, indent=4))

# 2. Create a function that checks if a website is up (returns True/False) with proper error handling

def is_website_up(url):
    try:
        response = requests.get(url, timeout=5)
        return response.status_code == 200
    except requests.RequestException as e:
        print(f"Error checking {url}: {e}")
        return False

# Example usage
website = "https://www.example.com"
print(f"Is {website} up? {is_website_up(website)}")


# 3. Write code that POSTs data to an API and handles different status codes appropriately

# API endpoint (using a public test API)
url = "https://jsonplaceholder.typicode.com/posts"

# Data to send in POST request
data = {
    "title": "DevOps Bootcamp",
    "body": "Learning API testing with Python and requests.",
    "userId": 1
}

print("Sending POST request...")

try:
    # Send POST request with JSON body
    response = requests.post(url, json=data)

    # Handle response based on status code
    if response.status_code == 201:
        print("✅ Resource created successfully!")
        print("Response JSON:", response.json())

    elif response.status_code == 200:
        print("✅ Request successful but no new resource created.")
        print("Response JSON:", response.json())

    elif response.status_code == 400:
        print("⚠️ Bad Request — The server could not understand the request.")

    elif response.status_code == 401:
        print("🔒 Unauthorized — Check authentication credentials.")

    elif response.status_code == 404:
        print("❌ Not Found — The requested URL or resource does not exist.")

    elif response.status_code == 500:
        print("💥 Server Error — Something went wrong on the server side.")

    else:
        print(f"❓ Unexpected status code: {response.status_code}")
        print("Response text:", response.text)

except requests.exceptions.RequestException as e:
    print("🚫 Request failed:", e)

# 4. Create a health check script that:
#    - Checks multiple service endpoints
#    - Measures response time
#    - Returns a summary report
#    - Sends an alert if any service is down

def service_health(name, url, timeout=5):
    try:
        start_time = datetime.now()
        response = requests.get(url, timeout=timeout)
        response_time = (datetime.now() - start_time).total_seconds()
        
        return {
            'name': name,
            'status': 'UP' if response.status_code == 200 else 'DOWN',
            'status_code': response.status_code,
            'response_time': f"{response_time:.2f}s",
            'error': None
        }
    except requests.RequestException as e:
        return {
            'name': name,
            'status': 'DOWN',
            'status_code': None,
            'response_time': None,
            'error': str(e)
        }

services = [
    ("JSONPlaceholder API", "https://jsonplaceholder.typicode.com/posts/1"),
    ("HTTPBin", "https://httpbin.org/status/200"),
    ("GitHub API", "https://api.github.com"),
]
results = []

for name, url in services:
    result = service_health(name, url)
    results.append(result)

    status_icon = "UP ✅" if result['status'] == 'UP' else "DOWN ❌"
    print(f"{name}: {status_icon} | Response Time: {result['response_time']} | Status Code: {result['status_code']} | Error: {result['error']}")

    if(result['status_code']):
        print(f"status code is {result['status_code']}")
        print(f"response time is {result['response_time']}")
    if(result['error']):
        print(f"error is {result['error']}")

up_count = sum(1 for r in results if r['status'] == 'UP')
print(f"\nSummary: {up_count}/{len(services)} services are UP.")

# 5. Write a function that downloads a file from a URL with:
#    - Progress indication
#    - Timeout handling
#    - Error handling

def download_file(url, filename):
    try:
        print(f"Starting download from: {url}")
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()  # Raise error for bad responses

        total_length = response.headers.get('content-length')

        with open(filename, 'wb') as file:
            if total_length is None:
                # No content length header — just write directly
                file.write(response.content)
            else:
                downloaded = 0
                total_length = int(total_length)
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        file.write(chunk)
                        downloaded += len(chunk)
                        done = int(50 * downloaded / total_length)
                        print(f"\r[{'=' * done}{' ' * (50 - done)}] {downloaded * 100 / total_length:.2f}%", end='')

        print(f"\n✅ Download completed: {filename}")

    except requests.exceptions.Timeout:
        print("⏱️ Download timed out.")
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP error: {e}")
    except requests.exceptions.ConnectionError:
        print("🌐 Connection error.")
    except Exception as e:
        print(f"🚫 Unexpected error: {e}")

# Example usage
if __name__ == "__main__":
    url = "https://raw.githubusercontent.com/vinta/awesome-python/master/README.md"
    download_file(url, "awesome_python_readme.md")

# 6. Create an API client class for JSONPlaceholder that:
#    - Has methods for GET, POST, PUT, DELETE
#    - Handles errors gracefully
#    - Includes logging

import requests
import logging

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class JSONPlaceholderClient:
    """Simple API client for JSONPlaceholder."""
    
    def __init__(self, base_url="https://jsonplaceholder.typicode.com"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({'Content-Type': 'application/json'})
    
    def _handle_response(self, response):
        """Private helper method to handle responses and log errors."""
        if response.status_code in (200, 201):
            logging.info(f"✅ Success ({response.status_code})")
            return response.json()
        elif response.status_code == 404:
            logging.error("❌ Not Found (404)")
        elif response.status_code == 400:
            logging.error("⚠️ Bad Request (400)")
        elif response.status_code >= 500:
            logging.error("💥 Server Error (5xx)")
        else:
            logging.warning(f"⚠️ Unexpected status: {response.status_code}")
        return None

    def get(self, endpoint):
        """GET request"""
        try:
            response = self.session.get(f"{self.base_url}/{endpoint}", timeout=5)
            return self._handle_response(response)
        except requests.RequestException as e:
            logging.error(f"GET request failed: {e}")

    def post(self, endpoint, data):
        """POST request"""
        try:
            response = self.session.post(f"{self.base_url}/{endpoint}", json=data, timeout=5)
            return self._handle_response(response)
        except requests.RequestException as e:
            logging.error(f"POST request failed: {e}")

    def put(self, endpoint, data):
        """PUT request"""
        try:
            response = self.session.put(f"{self.base_url}/{endpoint}", json=data, timeout=5)
            return self._handle_response(response)
        except requests.RequestException as e:
            logging.error(f"PUT request failed: {e}")

    def delete(self, endpoint):
        """DELETE request"""
        try:
            response = self.session.delete(f"{self.base_url}/{endpoint}", timeout=5)
            if response.status_code == 200:
                logging.info("✅ Deleted successfully")
                return True
            elif response.status_code == 404:
                logging.warning("⚠️ Resource not found")
            else:
                logging.error(f"❌ Delete failed with status {response.status_code}")
            return False
        except requests.RequestException as e:
            logging.error(f"DELETE request failed: {e}")

# Example usage
if __name__ == "__main__":
    client = JSONPlaceholderClient()

    print("\n➡️ GET /posts/1")
    post = client.get("posts/1")
    print(post)

    print("\n➡️ POST /posts")
    new_post = client.post("posts", {"title": "Hello", "body": "World", "userId": 1})
    print(new_post)

    print("\n➡️ PUT /posts/1")
    updated_post = client.put("posts/1", {"title": "Updated", "body": "Post body", "userId": 1})
    print(updated_post)

    print("\n➡️ DELETE /posts/1")
    client.delete("posts/1")


# 7.  Write code that makes parallel requests to multiple endpoints and collects results

import requests
import concurrent.futures

def fetch_url(url):
    """Fetch data from a single URL."""
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return {url: response.json()}
        else:
            return {url: f"Error: {response.status_code}"}
    except requests.RequestException as e:
        return {url: f"Failed: {e}"}

def fetch_all(urls):
    """Fetch multiple URLs in parallel."""
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        # Start all fetch tasks
        future_to_url = {executor.submit(fetch_url, url): url for url in urls}
        
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                data = future.result()
                results.append(data)
            except Exception as e:
                results.append({url: f"Error: {e}"})
    return results

# Example usage
if __name__ == "__main__":
    urls = [
        "https://jsonplaceholder.typicode.com/posts/1",
        "https://jsonplaceholder.typicode.com/posts/2",
        "https://jsonplaceholder.typicode.com/posts/3",
        "https://jsonplaceholder.typicode.com/posts/4",
        "https://jsonplaceholder.typicode.com/posts/5"
    ]
    
    print("🚀 Fetching data from multiple endpoints in parallel...\n")
    all_results = fetch_all(urls)
    
    for result in all_results:
        for url, data in result.items():
            print(f"{url} → {type(data)}")

# 8. Implement retry logic for failed requests (retry 3 times with exponential backoff)

import requests
import time

def get_with_retry(url, retries=3, backoff_factor=2):
    """
    Perform a GET request with retry logic and exponential backoff.
    :param url: URL to fetch
    :param retries: Number of retry attempts
    :param backoff_factor: Multiplier for backoff delay (e.g., 1, 2, 4 seconds)
    """
    attempt = 0
    while attempt < retries:
        try:
            print(f"Attempt {attempt + 1} → Fetching {url}")
            response = requests.get(url, timeout=5)

            # If the response is OK (200–299), return it
            if response.ok:
                print("✅ Request succeeded.")
                return response.json()
            else:
                print(f"⚠️ Request failed with status {response.status_code}")
        except requests.RequestException as e:
            print(f"❌ Error: {e}")

        # Wait before retrying (exponential backoff)
        attempt += 1
        sleep_time = backoff_factor ** attempt
        print(f"⏳ Retrying in {sleep_time} seconds...\n")
        time.sleep(sleep_time)

    print("❌ All retry attempts failed.")
    return None


# Example usage
if __name__ == "__main__":
    url = "https://jsonplaceholder.typicode.com/postss/1"
    data = get_with_retry(url)

    if data:
        print("\nFetched Data:")
        print(data)
    else:
        print("\nFailed to retrieve data after multiple retries.")


# 9. Build a monitoring script that:
    # - Checks API endpoints every 30 seconds
    # - Logs response times
    # - Alerts if response time > threshold
    # - Saves results to a file

def monitor_api(url, threshold=10, interval=30, duration=300):
    """
    Monitor an API endpoint for response times.
    :param url: API endpoint to monitor
    :param threshold: Response time threshold in seconds
    :param interval: Time between checks in seconds
    :param duration: Total monitoring duration in seconds
    """
    end_time = time.time() + duration
    log_file = "api_monitor_log.txt"

    with open(log_file, 'w') as f:
        f.write("Timestamp,Response Time (s),Status\n")

    while time.time() < end_time:
        start_time = time.time()
        try:
            response = requests.get(url, timeout=10)
            response_time = time.time() - start_time

            status = "OK" if response_time <= threshold else "ALERT"
            log_entry = f"{datetime.now()},{response_time:.2f},{status}\n"

            with open(log_file, 'a') as f:
                f.write(log_entry)

            print(f"{datetime.now()} | Response Time: {response_time:.2f}s | Status: {status}")

            if response_time > threshold:
                print(f"🚨 ALERT: Response time {response_time:.2f}s exceeds threshold of {threshold}s!")

        except requests.RequestException as e:
            print(f"❌ Error during request: {e}")

        time.sleep(interval)

# Example usage
if __name__ == "__main__":
    monitor_api("https://jsonplaceholder.typicode.com/posts/1", threshold=1, interval=30, duration=120)