FROM python:latest

WORKDIR /src

COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY ./src /src
COPY init.sh init.sh
COPY wait-for-it.sh wait-for-it.sh

RUN chmod +x wait-for-it.sh
RUN chmod +x init.sh

# CMD ["./init.sh"]
# CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]
