FROM python:latest

WORKDIR /app

COPY ./reader/requirements.txt .
COPY ./reader/src /app/src
COPY ./common /app/src/common

RUN pip install --upgrade pip && pip install -r requirements.txt

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8802", "--reload"]