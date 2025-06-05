FROM python:latest

WORKDIR /apps

COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /apps

CMD ["uvicorn", "apps.main:app", "--host", "0.0.0.0", "--port", "8007", "--reload"]