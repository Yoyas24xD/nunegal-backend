import asyncio
import logging

from fastapi import FastAPI, HTTPException, status
from models import SimilarProducts
from settings import API_URL
from utils import fetch_similar_product_ids, request

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
app = FastAPI()


@app.get("/product/{product_id}/similar", response_model=SimilarProducts)
async def get_similar_products(product_id: int):
    """
    Obtiene los productos similares a un producto dado por su ID.

    Args:
        product_id (int): El ID del producto del que se quieren obtener los similares.

    Returns:
        SimilarProducts: Un objeto que contiene la lista de productos similares.

    Raises:
        HTTPException: Si ocurre un error al hacer la petición a la API externa.
    """
    try:
        ids_data = await fetch_similar_product_ids(product_id)

        requests = [request(f"{API_URL}/product/{id}") for id in ids_data]
        results = await asyncio.gather(*requests)

        return [result for result in results if result is not None]
    except HTTPException:
        raise  # se propaga la excepción HTTPException
    except Exception as e:
        logger.exception(
            f"Error inesperado al procesar la solicitud de productos similares: {e}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error inesperado: {e}",
        )
