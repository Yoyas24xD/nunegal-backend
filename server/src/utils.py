import os
import logging
from typing import List, Optional

import httpx
from fastapi import HTTPException, status

logger = logging.getLogger(__name__)
API_URL = os.getenv("API_URL")


async def request(url: str) -> Optional[dict]:
    """
    Realiza una petición HTTP GET asíncrona a la URL especificada.

    Args:
        url (str): La URL a la que se va a hacer la petición.

    Returns:
        Optional[dict]: El JSON de la respuesta si la petición es exitosa, None en caso de error.

    Raises:
        httpx.TimeoutException: Si la petición excede el tiempo de espera.
        httpx.RequestError: Para errores generales de la petición (e.g., conexión rechazada).
        httpx.HTTPStatusError: Para respuestas con códigos de estado de error (4xx o 5xx).
        Exception: Para cualquier otro error inesperado.
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=10.0)
            response.raise_for_status()
            return response.json()
        except httpx.TimeoutException:
            return None
        except httpx.RequestError as e:
            logger.error(f"Error de petición al hacer la petición a {url}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al conectar con el servidor: {e}",
            ) from e
        except httpx.HTTPStatusError:
            return None
        except Exception as e:
            logger.exception(
                f"Error inesperado al hacer la petición a {url}: {e}"
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error inesperado: {e}",
            ) from e


async def fetch_similar_product_ids(product_id: int) -> List[int]:
    """
    Obtiene los IDs de productos similares a un producto dado por su ID.

    Args:
        product_id (int): El ID del producto del que se quieren obtener los similares.

    Returns:
        List[int]: Una lista de IDs de productos similares.

    Raises:
        HTTPException: Si ocurre un error al hacer la petición a la API externa.
    """

    ids_data = await request(f"{API_URL}/product/{product_id}/similarids")
    if ids_data is None:
        logger.warning(
            f"No se encontraron IDs de productos similares para el producto {product_id}"
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontraron productos similares para el producto con ID {product_id}",
        )

    if not isinstance(ids_data, list):
        logger.error(f"Se esperaba una lista de IDs, pero se recibió: {ids_data}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error inesperado: Se esperaba una lista de IDs de productos similares.",
        )

    return ids_data
