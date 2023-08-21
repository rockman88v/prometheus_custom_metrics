FROM python:3.10.2-slim-buster
WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY app-monitor.py .
# Set environment variables
#ENV DOMAIN="http://web-histogram:8080"
#ENV API1_PATH="/get-api1"
#ENV API2_PATH="/get-api2"
#ENV PORT=8081
EXPOSE 8082
ENTRYPOINT ["python", "app-monitor.py"]