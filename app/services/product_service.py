from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination import Page

from app.crud import product_crud
from app.schemas.product import Product, ProductRequest
from app.models.product import Product as ProductModel


async def get_products(db: AsyncSession, params: ProductRequest) -> Page[Product]:
    products_db: Page[ProductModel] = await product_crud.get_products(db=db, params=params)
    products: Page[Product] = Page[Product].model_validate(products_db)
    return products
