import requests
import random
import string
from joblib import Parallel, delayed

API_URL = "https://web-aca-app.icystone-a0aff22b.westus2.azurecontainerapps.io/process_event"

# Function to generate random user ID and event name
def generate_random_event():
    userid = "ron-test1"
    eventname = ''.join(random.choices(string.ascii_lowercase, k=10))
    return {"userid": userid, "eventname": eventname}

# Function to send the POST request to the FastAPI app
def send_event_request(event_data):
    response = requests.post(API_URL, json=event_data)
    return response.json()

# Generate random events
def generate_and_send_event():
    event_data = generate_random_event()
    return send_event_request(event_data)

# send 1000 POST requests in parallel
def send_parallel_requests():
    results = Parallel(n_jobs=-1)(delayed(generate_and_send_event)() for _ in range(1000))
    return results

if __name__ == "__main__":
    print("Sending 1000 POST requests to process_event...")
    results = send_parallel_requests()
    print("Finished sending requests!")

