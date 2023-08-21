FROM python:3.10.2-slim-buster
WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY b2b-monitor-realtime.py .
# Set environment variables
ENV PYTHONUNBUFFERED=1
#ENV CTN_PORT=8081
#ENV EXPORTED_JOB_NAME="PG.BDS.B2B.ProjectNetService-K8S.Client"
#ENV INTERVAL=5
#EXPOSE 8082
ENTRYPOINT ["python", "b2b-monitor-realtime.py"]