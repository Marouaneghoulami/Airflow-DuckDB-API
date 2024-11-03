import requests
import pandas as pd
from io import StringIO
import logging
from ..helpers.logging_helpers import setup_logging

# Set up logging
setup_logging()


def fetch_api_sales_data(**kwargs):
    """Fetch sales data from the Mockaroo API and return it as a DataFrame."""
    api_url = "https://my.api.mockaroo.com/all_sales"
    headers = {"X-API-Key": "f31a9510"}
    
    try:
        response = requests.get(api_url, headers=headers)
        if response.status_code != 200:
            raise ValueError(f"Error fetching data, status code: {response.status_code}")
        else:
            data = pd.read_csv(StringIO(response.text))
            # Convert DataFrame to a list of dictionaries
            data_dict = data.to_dict(orient="records")
            logging.info("Successfully fetched sales data from the API.")
            # Push data_dict to XCom
            kwargs['ti'].xcom_push(key='sales_data', value=data_dict)
    except Exception as e:
        logging.error(f"Failed to fetch data from API: {e}")
        raise


