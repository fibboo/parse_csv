from datetime import datetime
from uuid import UUID

from fastapi_pagination import Params
from pydantic import BaseModel, ConfigDict, conint, Field


class ProductBase(BaseModel):
    name: str
    photo_url: str | None = None
    barcode: str
    price_cents: conint(ge=0)
    producer: str | None = None


class ProductCreate(ProductBase):
    id: UUID  # noqa: A003


class ProductUpdate(ProductBase):
    pass


class Product(ProductBase):
    id: UUID  # noqa: A003

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProductRequest(Params):
    page: int = Field(1, ge=1, description='Page number')
    size: int = Field(20, ge=1, le=100, description='Page size')

    producer: str | None = None
