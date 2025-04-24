from typing import List

from pydantic import BaseModel, RootModel


class ProductDetail(BaseModel):
    id: str
    name: str
    price: float
    availability: bool


SimilarProducts = RootModel[List[ProductDetail]]
