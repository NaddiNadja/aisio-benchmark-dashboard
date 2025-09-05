# syntax=docker/dockerfile:1
FROM python:3.11.13-bookworm

WORKDIR /app

COPY . .
RUN echo "Time, Batches, IOPS, MiB/s\n0, 0, 0, 0" > posix.csv
RUN echo "Time, Batches, IOPS, MiB/s\n0, 0, 0, 0" > gds.csv
RUN echo "Time, Batches, IOPS, MiB/s\n0, 0, 0, 0" > aisio.csv

RUN pip install -r requirements.txt

EXPOSE 4000
CMD ["python3", "-u", "server.py"]