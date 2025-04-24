import os
from unittest import mock

import pytest
from fastapi import HTTPException, status
from fastapi.testclient import TestClient

from main import app  # Asegúrate de que la ruta al archivo main.py es correcta

client = TestClient(app)


@pytest.fixture
def mock_fetch_similar_product_ids():
    with mock.patch("main.fetch_similar_product_ids") as mock_func:
        yield mock_func


@pytest.fixture
def mock_request():
    with mock.patch("main.request") as mock_func:
        yield mock_func


@pytest.fixture(scope="module", autouse=True)
def mock_api_url():
    with mock.patch("main.API_URL", "None"):
        yield


def test_get_similar_products_success(mock_fetch_similar_product_ids, mock_request):
    product_id = 123
    mock_fetch_similar_product_ids.return_value = [456, 789]
    mock_request.side_effect = [
        {
            "id": "456",
            "name": "Producto Similar 1",
            "price": 25.99,
            "availability": True,
        },
        {
            "id": "789",
            "name": "Producto Similar 2",
            "price": 19.99,
            "availability": False,
        },
    ]

    response = client.get(f"/product/{product_id}/similar")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            "id": "456",
            "name": "Producto Similar 1",
            "price": 25.99,
            "availability": True,
        },
        {
            "id": "789",
            "name": "Producto Similar 2",
            "price": 19.99,
            "availability": False,
        },
    ]
    mock_fetch_similar_product_ids.assert_called_once_with(product_id)
    assert mock_request.call_count == 2
    mock_request.assert_any_call("None/product/456")
    mock_request.assert_any_call("None/product/789")


def test_get_similar_products_empty_list(mock_fetch_similar_product_ids):
    product_id = 123
    mock_fetch_similar_product_ids.return_value = []

    response = client.get(f"/product/{product_id}/similar")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []
    mock_fetch_similar_product_ids.assert_called_once_with(product_id)


def test_get_similar_products_fetch_ids_error(mock_fetch_similar_product_ids):
    product_id = 123
    mock_fetch_similar_product_ids.side_effect = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Productos similares no encontrados",
    )

    response = client.get(f"/product/{product_id}/similar")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Productos similares no encontrados"}
    mock_fetch_similar_product_ids.assert_called_once_with(product_id)


def test_get_similar_products_request_error(
    mock_fetch_similar_product_ids, mock_request
):
    product_id = 123
    mock_fetch_similar_product_ids.return_value = [456]
    mock_request.side_effect = HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Error en API externa"
    )

    with mock.patch.dict(os.environ, {"API_URL": "None"}):
        response = client.get(f"/product/{product_id}/similar")

        assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
        assert response.json() == {"detail": "Error en API externa"}
        mock_fetch_similar_product_ids.assert_called_once_with(product_id)
        mock_request.assert_called_once_with("None/product/456")


def test_get_similar_products_unexpected_error(mock_fetch_similar_product_ids):
    product_id = 123
    mock_fetch_similar_product_ids.side_effect = ValueError("Error inesperado")

    response = client.get(f"/product/{product_id}/similar")

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert "Error inesperado" in response.json()["detail"]
    mock_fetch_similar_product_ids.assert_called_once_with(product_id)
