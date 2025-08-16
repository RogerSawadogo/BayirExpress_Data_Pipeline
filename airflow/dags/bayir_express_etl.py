from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from etl.extract import extract_collection
from etl.transform import clean_users, clean_annonces
from etl.load import load_to_csv

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    "bayir_express_etl",
    default_args=default_args,
    description="Extraction MongoDB, nettoyage et export CSV pour BayirExpress",
    schedule_interval="@daily",
    start_date=datetime(2025, 8, 1),
    catchup=False,
    tags=["mongo", "csv", "ETL"]
) as dag:

    def etl_users():
        df = extract_collection("users")
        df = clean_users(df)
        load_to_csv(df, "users.csv")

    def etl_annonces():
        df = extract_collection("annonces")
        df = clean_annonces(df)
        load_to_csv(df, "annonces.csv")

    task_users = PythonOperator(
        task_id="etl_users",
        python_callable=etl_users
    )

    task_annonces = PythonOperator(
        task_id="etl_annonces",
        python_callable=etl_annonces
    )

    task_users >> task_annonces
