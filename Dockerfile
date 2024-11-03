FROM python:3.9-slim

WORKDIR /app

RUN apt-get update --fix-missing && \
    apt-get install -y python3 python3-pip python3-venv stress-ng iperf3 sysbench && \
    rm -rf /var/lib/apt/lists/*

RUN python3 -m venv /app/venv

COPY main.py /app

RUN /app/venv/bin/pip install --no-cache-dir psutil

ENV PATH="/app/venv/bin:$PATH"

ENTRYPOINT ["python", "main.py"]
