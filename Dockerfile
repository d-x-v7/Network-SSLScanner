FROM python:3.7.3 AS builder
COPY requirements.txt

RUN pip install --user -r requirements.txt


FROM python:3.7.3-slim
