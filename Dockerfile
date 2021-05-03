FROM python:3.7 AS builder
COPY requirements.txt .

RUN pip install -r requirements.txt

FROM python:3.7.3-slim
WORKDIR /SSLWebScanner

CMD [ "python"]