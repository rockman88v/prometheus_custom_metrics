import os
import time
import requests
import threading
import json
from prometheus_client import Histogram, generate_latest, CONTENT_TYPE_LATEST
from flask import Flask

app = Flask(__name__)

# Read environment variables
DOMAIN = os.environ.get("DOMAIN", "https://poc-projectnet.staging.propertyguru.vn")
#API1_PATH = os.environ.get("API1_PATH", "/api/tests/faqs/64")
CTN_PORT = int(os.environ.get("CTN_PORT", 8182))
EXPORTED_JOB_NAME = os.environ.get("EXPORTED_JOB_NAME", "PG.BDS.B2B.ProjectNetService-K8S.Client")
INTERVAL = int(os.environ.get("INTERVAL", 5))

# Define histogram metric
http_client_histogram = Histogram(
    "http_server_duration",
    "HTTP server request duration histogram",
    ["http_status_code", "http_response_size", "http_method", "http_target", "api_name","exported_job","http_scheme"],
    buckets=(0, 5, 10, 25, 50, 75, 100, 250, 500, 750, 1000, 2500, 5000, 7500, 10000),
)

def call_api():
    while True:
        try:
            detail_faqs()
            find_faqs()
            save_faqs()
            add_faqs()
            # Log the information
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"{current_time}\t PG.BDS.B2B.ProjectNetService-K8S.Client success")

        except requests.exceptions.RequestException as e:
            # Log error details if an exception occurs
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
            error_detail = str(e)            
            print(f"{current_time}\t PG.BDS.B2B.ProjectNetService-K8S.Client \tError:{error_detail}")
        time.sleep(INTERVAL)

@app.route("/healthcheck")
def health_check():
    return "OK", 200

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}

def detail_faqs():
    # Make requests and collect metrics for API "B2B_DETAIL_FAQS"
    api_name = "B2B_DETAIL_FAQS"
    #domain = "https://poc-projectnet.staging.propertyguru.vn"
    domain = DOMAIN
    api_path = "/api/tests/faqs/64"
    url = domain + api_path
    payload = {}
    headers = {}
    start_time = time.time()
    response = requests.request("GET", url, headers=headers, data=payload)        
    end_time = time.time()
    #response_time = end_time - start_time
    response_time_ms = (end_time - start_time) * 1000
    labels = {
            "http_status_code": response.status_code,
            "http_response_size": len(response.content),
            "http_method": "GET",
            "http_target": api_path,
            "api_name": api_name,
            "exported_job": EXPORTED_JOB_NAME,
            "http_scheme": "http",
        }
    http_client_histogram.labels(**labels).observe(response_time_ms)
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    response_code = response.status_code
    print(f"{current_time}\t PG.BDS.B2B.ProjectNetService-K8S.Client\tAPI={api_name}\tResponseCode={response_code}\tResponseTime={response_time_ms:.3f} ms")    
        
    return "Requests made and metrics recorded"

def find_faqs():
    # Make requests and collect metrics for API "B2B_FIND_FAQS"    
    api_name = "B2B_FIND_FAQS"
    #domain = "https://poc-projectnet.staging.propertyguru.vn"
    domain = DOMAIN
    api_path = "/api/tests/faqs/find"
    url = domain + api_path    
    payload = json.dumps({
        "queryParams": {
            "filter": {
            "productType": -2,
            "cateId": -1,
            "cityCode": "SELECTCITY",
            "districtId": -2,
            "wardId": -2,
            "streetId": -2,
            "projectId": -2,
            "pageUrl": "",
            "priceType": -2,
            "minPrice": None,
            "maxPrice": None
            },
            "sortOrder": "desc",
            "sortField": "ProductId",
            "pageNumber": 1,
            "pageSize": 10
        }
        })
    headers = {
  'Content-Type': 'application/json'
}
    start_time = time.time()
    response = requests.request("POST", url, headers=headers, data=payload)        
    end_time = time.time()
    #response_time = end_time - start_time    
    response_time_ms = (end_time - start_time) * 1000
    labels = {
            "http_status_code": response.status_code,
            "http_response_size": len(response.content),
            "http_method": "POST",
            "http_target": api_path,
            "api_name": api_name,
            "exported_job": EXPORTED_JOB_NAME,
            "http_scheme": "http",
        }
    http_client_histogram.labels(**labels).observe(response_time_ms)
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    response_code = response.status_code
    print(f"{current_time}\t PG.BDS.B2B.ProjectNetService-K8S.Client\tAPI={api_name}\tResponseCode={response_code}\tResponseTime={response_time_ms:.3f} ms")
    return "Requests made and metrics recorded."

def save_faqs():
    # Make requests and collect metrics for API "B2B_SAVE_FAQS"    
    api_name = "B2B_SAVE_FAQS"
    #domain = "https://poc-projectnet.staging.propertyguru.vn"
    domain = DOMAIN
    api_path = "/api/tests/faqs/64"
    url = domain + api_path    
    payload = json.dumps({
  "queryParams": {
    "productType": 38,
    "projectId": 20272,
    "cateId": 325,
    "cityCode": "SG",
    "districtId": 72,
    "wardId": 0,
    "streetId": 0,
    "pageType": {
      "id": 38,
      "name": "SRP Bán"
    },
    "cate": {
      "id": 325,
      "name": "Bán nhà biệt thự, liền kề"
    },
    "city": {
      "id": "SG",
      "name": "Hồ Chí Minh"
    },
    "district": {
      "id": 72,
      "name": "Huyện Bình Chánh"
    },
    "ward": {
      "id": 0,
      "name": "Không áp dụng"
    },
    "street": {
      "id": 0,
      "name": "Không áp dụng"
    },
    "project": {
      "id": 20272,
      "name": "The Mansion"
    },
    "priceType": {
      "id": 1,
      "name": "Sử dụng Min - Max"
    },
    "stage": 0,
    "uniqueHash": "2KmPdvSyW+C+/j3ed8hUPksqQ8SSfO21BOEYU1ZXujfi4jToEzvs+0oV4nnlY56Ygq6+vfdxqRlDb2EM9Tv/YAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=",
    "questions": [
      {
        "faqId": 209,
        "question": "TEST 1",
        "answer": "<p>TEST 1</p>",
        "productFaqId": 0
      },
      {
        "faqId": 0,
        "productId": 0,
        "question": "TEST2",
        "answer": "<p>tEST2</p>"
      }
    ],
    "createdBy": None,
    "updatedBy": None,
    "productId": 61,
    "location": "SRP Bán - Bán nhà biệt thự, liền kề - Hồ Chí Minh - Huyện Bình Chánh - The Mansion",
    "pageUrl": "",
    "priceTypeId": 1,
    "minPrice": 20,
    "maxPrice": 50,
    "price": None,
    "faqCount": 1
  }
})
    headers = {
  'Content-Type': 'application/json'
}
    start_time = time.time()
    response = requests.request("PUT", url, headers=headers, data=payload)        
    end_time = time.time()
    #response_time = end_time - start_time    
    response_time_ms = (end_time - start_time) * 1000
    labels = {
            "http_status_code": response.status_code,
            "http_response_size": len(response.content),
            "http_method": "PUT",
            "http_target": api_path,
            "api_name": api_name,
            "exported_job": EXPORTED_JOB_NAME,
            "http_scheme": "http",
        }
    http_client_histogram.labels(**labels).observe(response_time_ms)
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    response_code = response.status_code
    print(f"{current_time}\t PG.BDS.B2B.ProjectNetService-K8S.Client\tAPI={api_name}\tResponseCode={response_code}\tResponseTime={response_time_ms:.3f} ms")
    return "Requests made and metrics recorded."

def add_faqs():
    # Make requests and collect metrics for API "B2B_ADD_FAQS"    
    api_name = "B2B_ADD_FAQS"
    #domain = "https://poc-projectnet.staging.propertyguru.vn"
    domain = DOMAIN
    api_path = "/api/tests/faqs"
    url = domain + api_path
    payload = json.dumps({
    "queryParams": {
        "productId": 0,
        "location": "",
        "pageUrl": "",
        "faqCount": 0,
        "stage": 0,
        "productType": 38,
        "price": "",
        "pageType": {
        "id": 38,
        "name": "Bán"
        },
        "cate": {
        "id": 327,
        "name": "Bán căn hộ chung cư"
        },
        "city": {
        "id": "SG",
        "name": "Hồ Chí Minh"
        },
        "district": {
        "id": 72,
        "name": "Huyện Bình Chánh"
        },
        "ward": {
        "id": 0,
        "name": ""
        },
        "street": {
        "id": 0,
        "name": ""
        },
        "project": {
        "id": 20215,
        "name": "Khu dân cư Saigonres"
        },
        "priceType": {
        "id": 1,
        "name": "Sử dụng Min - Max"
        },
        "minPrice": 10,
        "maxPrice": 50,
        "questions": [
        {
            "faqId": 0,
            "productId": 0,
            "question": "TEST 1",
            "answer": "<p>TEST 1</p>"
        }
        ]
    }
    })
    headers = {
  'Content-Type': 'application/json'
}
    start_time = time.time()
    response = requests.request("POST", url, headers=headers, data=payload)        
    end_time = time.time()
    #response_time = end_time - start_time    
    response_time_ms = (end_time - start_time) * 1000
    labels = {
            "http_status_code": response.status_code,
            "http_response_size": len(response.content),
            "http_method": "POST",
            "http_target": api_path,
            "api_name": api_name,
            "exported_job": EXPORTED_JOB_NAME,
            "http_scheme": "http",
        }
    http_client_histogram.labels(**labels).observe(response_time_ms)
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    response_code = response.status_code
    print(f"{current_time}\t PG.BDS.B2B.ProjectNetService-K8S.Client\tAPI={api_name}\tResponseCode={response_code}\tResponseTime={response_time_ms:.3f} ms")
    return "Requests made and metrics recorded"

if __name__ == "__main__":
    # Start the call_api function in a separate thread
    info_thread = threading.Thread(target=call_api)
    info_thread.daemon = True
    info_thread.start()

    # Run the Flask app
    app.run(host="0.0.0.0", port=CTN_PORT)
