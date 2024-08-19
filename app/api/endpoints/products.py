from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination import Page

from app.api.deps import get_db
from app.schemas.product import Product, ProductRequest
from app.services import product_service

router = APIRouter()


@router.post('')
async def get_products(params: ProductRequest, db: AsyncSession = Depends(get_db)) -> Page[Product]:
    products: Page[Product] = await product_service.get_products(db=db, params=params)
    return products
