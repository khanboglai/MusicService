FROM python:latest

WORKDIR /src

COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /src

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8005", "--reload"]