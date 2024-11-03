from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.sensors.external_task import ExternalTaskSensor
from datetime import datetime, timedelta
import duckdb
import logging

# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                            logging.FileHandler("db_setup.log"),
                            logging.StreamHandler()])

# Function to select specific fields and insert into another table
def select_and_insert():
    # Define DuckDB connection
    duckdb_path = 'db/ecommerce_data.db'
    conn = duckdb.connect(duckdb_path)

    try:
        # Select specific fields from the source table
        result = conn.execute("""
            SELECT customer_id, customer_name, email, gender, country_code
            FROM raw_layer.sales
        """).fetchall()

        # Insert the selected fields into the destination table
        for row in result:
            conn.execute("""
                INSERT INTO refined_layer.customers (customer_id, customer_name, email, gender, country_code)
                VALUES (?, ?, ?, ?, ?)
            """, row)

        logging.info("Data successfully selected and inserted into refined_layer.customers.")

    except Exception as e:
        logging.error(f"Error during data selection and insertion: {e}")
        raise

    finally:
        conn.close()

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=5),
    'start_date': datetime(2024, 11, 1),
}

with DAG(
    'load_customers_data_to_db',
    default_args=default_args,
    description='Load data to customes tabler',
    #schedule_interval='@daily',
    catchup=False
) as dag:

    # Sensor to wait for DAG A to complete
    wait_for_sales_raw_dag = ExternalTaskSensor(
        task_id='wait_for_dag_load_sales_data_to_db',
        external_dag_id='load_sales_data_to_db',
        external_task_id='store_sales_data_raw',  # Task in DAG A to wait for
        mode='poke',  # or 'reschedule'
        timeout=600,  # Timeout after 10 minutes
        poke_interval=60  # Check every minute
    )

    # Task to select and insert data
    insert_data_task = PythonOperator(
        task_id='select_and_insert_customers_refined',
        python_callable=select_and_insert
    )

    # Set the task dependencies
    wait_for_sales_raw_dag >> insert_data_task
