from datetime import datetime
import pandas as pd
import duckdb
import logging
from ..helpers.logging_helpers import setup_logging
from ..helpers.database_helpers import connect_db, close_db, insert_data

# Set up logging
setup_logging()

def store_api_sales_data(**kwargs):
    """Store the fetched sales data into DuckDB raw_layer.sales table."""
    data_dict = kwargs['ti'].xcom_pull(key='sales_data', task_ids='fetch_sales_data_raw')
    # Convert list of dictionaries to a DataFrame
    data = pd.DataFrame(data_dict)
    # Define DuckDB connection and schema
    duckdb_path = 'db/ecommerce_data.db'
    conn = connect_db(duckdb_path)
    
    # Write data to DuckDB table
    try:
        ingestion_time = datetime.now()
        columns = [
            "order_id", "order_date", "quantity", "payment_method", "order_status",
            "customer_id", "customer_name", "email", "gender", "country_code",
            "product_id", "product_name", "unit_price", "ingestion_time"
        ]
        records = [(
                record["order_id"], record["order_date"], record["quantity"], record["payment_method"],
                record["order_status"], record["customer_id"], record["customer_name"],
                record["email"], record["gender"], record["country_code"], record["product_id"],
                record["product_name"], record["unit_price"], record["ingestion_time"]
            ) for record in data
        ]
        # Insert data using the generic insert function
        insert_data(conn, "raw_layer.sales", columns, records)

        logging.info("Data successfully inserted into DuckDB raw_layer.sales table.")
    
    except Exception as e:
        logging.error(f"Failed to insert data into DuckDB: {e}")
        raise
    finally:
        close_db()
        logging.info("Closed DuckDB connection.")