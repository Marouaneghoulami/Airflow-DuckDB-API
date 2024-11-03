from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
import pandas as pd
import duckdb
import logging
from io import StringIO
from logic import raw_fetch_sales_api as rfsa
from logic import raw_store_sales_data as rssd


# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                            logging.FileHandler("db_setup.log"),
                            logging.StreamHandler()])

# Set up default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=5),
    'start_date': datetime(2024, 11, 1),
}

# Define the DAG
with DAG(
    'raw_api_sales_data',
    default_args=default_args,
    description='load sales data from sales API to DuckDB',
    #schedule_interval='*/10 * * * *',  # Schedule to run every minute; adjust as needed
    catchup=False
) as dag:

    # Define PythonOperator to store sales data to DuckDB
    fetch_api_sales_data_task = PythonOperator(
        task_id='01_fetch_api_sales_data_task',
        python_callable=rfsa.fetch_api_sales_data
    )
    
    store_api_sales_data_task = PythonOperator(
        task_id='02_store_api_sales_data_task',
        python_callable=rssd.store_api_sales_data
    )

    fetch_data_task >> store_data_task
