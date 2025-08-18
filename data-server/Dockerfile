# syntax=docker/dockerfile:1
FROM python:3.11.13-bookworm

ARG SOURCE

WORKDIR /app

COPY . .
RUN cp /app/data/${SOURCE}.csv /app/data.csv
RUN cp /app/data/${SOURCE}.csv /app/pregenerated.csv

RUN pip install -r requirements.txt

EXPOSE 4000
CMD ["python3", "-u", "server.py"]