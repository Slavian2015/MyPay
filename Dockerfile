FROM python:3.6-buster

WORKDIR /MyPay
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD ["python", "app.py"]