FROM apache/airflow:3.0.3

USER root

RUN apt-get update && apt-get install -y \
        python3-pip \
        python3-dev \
        build-essential \
    && pip3 install --upgrade pip \
    && pip3 install --no-cache-dir pandas numpy matplotlib \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER airflow


