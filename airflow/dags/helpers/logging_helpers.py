# config.py
import logging

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("db_setup.log"),
            logging.StreamHandler()
        ]
    )
    logging.info("Logging is set up.")

# Call setup_logging() at the start of any main script or function to initialize logging
