import duckdb
from typing import List, Dict
import logging
from .logging_helpers import setup_logging

# Set up logging
setup_logging()

def connect_db(db_path: str):
    """Connect to the DuckDB database."""
    try:
        conn = duckdb.connect(db_path)
        logging.info("Connected to DuckDB database.")
        return conn
    except Exception as e:
        logging.error(f"Failed to connect to the database: {e}")
        raise

def close_db(conn):
    """Close the database connection."""
    if conn:
        conn.close()
        logging.info("Closed the database connection.")

def add_schema(conn, schemas: List[str]):
    """Create schemas if they do not already exist."""
    for schema in schemas:
        try:
            conn.execute(f"CREATE SCHEMA IF NOT EXISTS {schema};")
            logging.info(f"Created schema '{schema}' if it did not exist.")
        except Exception as e:
            logging.error(f"Failed to create schema '{schema}': {e}")
            raise

def create_table(conn, schema: str, table: str, columns: Dict[str, str]):
    """Create a table with specified columns if it does not exist."""
    columns_def = ", ".join([f"{name} {type}" for name, type in columns.items()])
    create_table_sql = f"CREATE TABLE IF NOT EXISTS {schema}.{table} ({columns_def});"
    try:
        conn.execute(create_table_sql)
        logging.info(f"Created table '{schema}.{table}' with columns: {columns}.")
    except Exception as e:
        logging.error(f"Failed to create table '{schema}.{table}': {e}")
        raise

def add_column_if_not_exists(conn, schema: str, table: str, column: str, col_type: str):
    """Add a column to a table if it does not already exist."""
    try:
        col_exists_query = f"""
            SELECT COUNT(*)
            FROM information_schema.columns
            WHERE table_schema = '{schema}' AND table_name = '{table}' AND column_name = '{column}';
        """
        col_exists = conn.execute(col_exists_query).fetchone()[0] > 0
        if not col_exists:
            conn.execute(f"ALTER TABLE {schema}.{table} ADD COLUMN {column} {col_type};")
            logging.info(f"Added column '{column}' to table '{schema}.{table}'.")
        else:
            logging.info(f"Column '{column}' already exists in table '{schema}.{table}'.")
    except Exception as e:
        logging.error(f"Failed to add column '{column}' to table '{schema}.{table}': {e}")
        raise

def insert_data(conn, table_name, columns, records):
    """
    Inserts data into a specified DuckDB table.
    
    Parameters:
        conn (duckdb.DuckDBPyConnection): Connection object to DuckDB.
        table_name (str): The name of the table to insert data into.
        columns (list): List of column names as strings.
        records (list): List of tuples, each representing a row of data.
    """
    # Construct the column names and placeholder strings for the query
    columns_str = ', '.join(columns)
    placeholders = ', '.join(['?' for _ in columns])

    # SQL query to insert data
    query = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"
    
    try:
        # Execute the query for each record
        conn.executemany(query, records)
        logging.info(f"Data successfully inserted into {table_name}.")
    except Exception as e:
        logging.error(f"Failed to insert data into {table_name}: {e}")
        raise