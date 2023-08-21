import time
import random
from flask import Flask
from prometheus_client import Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# Define histogram metrics for API response times
get_api1 = Histogram(
    "get_api1_response_time_seconds",
    "Response time histogram for get-api1 API",
    ["path"],
)

# Define histogram metrics for API response times
get_api2 = Histogram(
    "get_api2_response_time_seconds",
    "Response time histogram for get-api2 API",
    ["path"],
)

# /get-api1 API endpoint
@app.route("/get-api1")
def function_api1():
    start_time = time.time()
    sleep_time = random.uniform(0.1, 0.15)  # Random sleep between 10-30 ms
    time.sleep(sleep_time)
    get_api1.labels(path="/get-api1").observe(time.time() - start_time)
    return "get-api1 result\n"

# /get-api2 API endpoint
@app.route("/get-api2")
def function_api2():
    start_time = time.time()
    sleep_time = random.uniform(0.2, 0.25)  # Random sleep between 10-30 ms
    time.sleep(sleep_time)
    get_api2.labels(path="/get-api2").observe(time.time() - start_time)
    return "get-api2 result\n"

# Expose metrics at /metrics endpoint
@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)  # Main API runs on port 8080
