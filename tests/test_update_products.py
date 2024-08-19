from uuid import UUID

import pytest
from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Product
from app.scripts import update_products


@pytest.mark.asyncio
async def test_update_db_from_csv(db_fixture: AsyncSession):
    # Arrange
    csv_file_path = 'data.csv'

    # Act
    await update_products._update_products_from_csv(db=db_fixture, file_path=csv_file_path)

    # Assert
    query: Select = select(Product)
    products: list[Product] = (await db_fixture.execute(query)).scalars().all()
    assert len(products) == 1000


@pytest.mark.asyncio
async def test_update_db_from_csv_update(db_fixture: AsyncSession, db_fixture2: AsyncSession):
    # Arrange
    csv_file_path = 'data.csv'
    csv_file_path_update = 'data_only_update.csv'
    product_ids: list[UUID] = [UUID('0285b967-261a-4a95-a21c-5c797ac7c0a2'),
                               UUID('0d9803c2-d16d-4f38-826c-f9869f619166')]
    await update_products._update_products_from_csv(db=db_fixture, file_path=csv_file_path)

    query_by_ids: Select = select(Product).where(Product.id.in_(product_ids))
    products_before: list[Product] = (await db_fixture.execute(query_by_ids)).scalars().all()

    # Act
    await update_products._update_products_from_csv(db=db_fixture2, file_path=csv_file_path_update)

    # Assert
    query: Select = select(Product)
    products: list[Product] = (await db_fixture2.execute(query)).scalars().all()
    assert len(products) == 1000

    products_after: list[Product] = (await db_fixture2.execute(query_by_ids)).scalars().all()
    assert len(products_after) == len(products_before) == 2
    assert products_after[0].name == 'Tea - Camomele (Updated)' != products_before[0].name
    assert products_after[0].photo_url == products_before[0].photo_url
    assert products_after[0].barcode == products_before[0].barcode
    assert products_after[0].price_cents == products_before[0].price_cents
    assert products_after[0].producer == products_before[0].producer
    assert products_after[0].created_at == products_before[0].created_at
    assert products_after[0].updated_at != products_before[0].updated_at
    assert products_after[1].name == products_before[1].name
    assert products_after[1].photo_url == 'http://dummyimage.com/ffffff_udated' != products_before[1].photo_url
    assert products_after[1].barcode == products_before[1].barcode
    assert products_after[1].price_cents == products_before[1].price_cents
    assert products_after[1].producer == products_before[1].producer
    assert products_after[1].created_at == products_before[1].created_at
    assert products_after[1].updated_at != products_before[1].updated_at
