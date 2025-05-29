FROM python:latest

WORKDIR /app

COPY ./writer/requirements.txt .
COPY ./writer/src /app/src
COPY ./common /app/src/common

RUN pip install --upgrade pip && pip install -r requirements.txt

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8801", "--reload"]