from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import Insert, Select, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductRequest


async def upsert_products(db: AsyncSession, create_data: list[ProductCreate]) -> None:
    create_data: list[dict] = [product.model_dump() for product in create_data]
    query: Insert = insert(Product).values(create_data)

    update_dict: dict = {c.name: query.excluded[c.name] for c in Product.__table__.c if
                         c.name not in ['id', 'created_at']}

    query = query.on_conflict_do_update(index_elements=['id'], set_=update_dict)

    await db.execute(query)
    await db.commit()


async def get_products(db: AsyncSession, params: ProductRequest) -> Page[Product]:
    query: Select = select(Product)
    if params.producer is not None and len(params.producer) > 3:
        query = query.where(Product.producer.ilike(f'%{params.producer}%'))

    products: Page[Product] = await paginate(db, query, params)
    return products
