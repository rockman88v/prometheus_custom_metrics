import os
import time
import requests
from prometheus_client import Histogram, generate_latest, CONTENT_TYPE_LATEST
from flask import Flask

app = Flask(__name__)

# Read environment variables
DOMAIN = os.environ.get("DOMAIN", "http://localhost")
API1_PATH = os.environ.get("API1_PATH", "/get-product")
API2_PATH = os.environ.get("API2_PATH", "/product-detail")
PORT = int(os.environ.get("PORT", 8081))

# Define histogram metric
http_client_histogram = Histogram(
    "http_client_duration",
    "HTTP client request duration histogram",
    ["http_response_code", "http_response_size", "http_method", "http_target"],
)

def make_request(url, target_path):
    start_time = time.time()
    response = requests.get(url + target_path)
    end_time = time.time()
    response_time = end_time - start_time
    return response, response_time

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}

@app.route("/call")
def main():
    api1_url = DOMAIN # + API1_PATH
    api2_url = DOMAIN # + API2_PATH

    # Make requests and collect metrics
    for api_url, api_path in [(api1_url, API1_PATH), (api2_url, API2_PATH)]:
        print(f"API URL: {api_url}, API Path: {api_path}")
        response, response_time = make_request(api_url, api_path)
        
        labels = {
            "http_response_code": response.status_code,
            "http_response_size": len(response.content),
            "http_method": "GET",
            "http_target": api_path,
        }
        
        print(f"API URL: {api_url}, API Path: {api_path}, Response Status Code: {response.status_code}")
        http_client_histogram.labels(**labels).observe(response_time)

    return "Requests made and metrics recorded."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
