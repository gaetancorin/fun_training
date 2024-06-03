from airflow import DAG
from airflow.decorators import task
from datetime import datetime
from passlib.hash import bcrypt
import os
import json

DATA_DIR = "/opt/airflow/data"
os.makedirs(DATA_DIR, exist_ok=True)

with DAG(
    dag_id="password_hashing_testing",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
):

    @task()
    def store_password():
        """Hash a password (simulate input)"""
        password = "MySecretPassword123"  # simulate input
        hashed = bcrypt.hash(password)
        hash_path = os.path.join(DATA_DIR, "password_hash.json")
        with open(hash_path, "w") as f:
            json.dump({"hash": hashed, "password": password}, f)
        print(f"✅ Password hashed and stored in {hash_path}")
        return hash_path


    hash_path = store_password()
