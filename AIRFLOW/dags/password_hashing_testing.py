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
        password = "MySecretPassword123"  # simulate input
        hashed = bcrypt.hash(password)
        hash_path = os.path.join(DATA_DIR, "password_hash.json")
        with open(hash_path, "w") as f:
            json.dump({"hash": hashed, "password": password}, f)
        print(f"✅ Password hashed and stored in {hash_path}")
        return hash_path

    @task()
    def verify_password(hash_path: str):
        with open(hash_path) as f:
            data = json.load(f)
        hashed = data["hash"]
        password = data["password"]

        ok = bcrypt.verify(password, hashed)
        print("Password correct" if ok else "Password incorrect")

        result_path = os.path.join(DATA_DIR, "password_verify.json")
        with open(result_path, "w") as f:
            json.dump({"verified": ok}, f)
        return result_path

    @task()
    def print_result(result_path: str):
        print(f"Verification results saved to {result_path}")

    hash_path = store_password()
    result_path = verify_password(hash_path)
    print_result(result_path)
