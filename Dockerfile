FROM python:3.10

WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY src/flask_api.py src/worker.py src/jobs.py ./
CMD ["python3"]