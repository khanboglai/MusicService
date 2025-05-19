FROM python:latest

WORKDIR /application

COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /app

# CMD [ "python3", "api/main.py" ]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--log-config=logger/log_conf.yaml"]