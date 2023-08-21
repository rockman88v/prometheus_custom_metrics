FROM python:3.10.2-slim-buster
WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY webserver.py .
EXPOSE 8080
ENTRYPOINT ["python", "webserver.py"]