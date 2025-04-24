import dotenv
import os
import logging

logger = logging.getLogger(__name__)

dotenv.load_dotenv()
API_URL = os.getenv("API_URL")

if API_URL is None:
    logger.critical("API_URL no está configurada en las variables de entorno.")
    raise ValueError("API_URL no está configurada en las variables de entorno.")

TIMEOUT = 5.0