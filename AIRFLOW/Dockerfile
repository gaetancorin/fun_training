FROM apache/airflow:3.0.3

USER root

# --- Install Python build tools and dependencies ---
RUN apt update && \
    apt-get install -y python3-pip python3-dev build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

USER airflow

# --- Install Python libraries ---
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir pandas numpy matplotlib