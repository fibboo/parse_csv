from uuid import uuid4

import pytest
from fastapi_pagination import Page
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import product_crud
from app.models.product import Product as ProductModel
from app.schemas.product import Product, ProductRequest


@pytest.mark.asyncio
async def test_get_products(db_fixture: AsyncSession):
    # Arrange
    create_data: list[ProductModel] = []
    for i in range(5):
        if i == 2:
            producer: str = 'Nothing'
        elif i == 0:
            producer = None
        else:
            producer: str = f'Producer {i}'
        create_data.append(ProductModel(id=uuid4(),
                                        name=f'Product {i}',
                                        photo_url=f'http://dummyimage.com/600x400/000/fff&text={i}',
                                        barcode=f'barcode {i}',
                                        price_cents=i * 100,
                                        producer=producer))

    db_fixture.add_all(create_data)
    await db_fixture.commit()

    params_no_filter = ProductRequest()
    params_one_product = ProductRequest(producer='Producer 1')
    params_part = ProductRequest(producer='thin')
    params_multiple_products = ProductRequest(producer='Producer')
    params_no_results = ProductRequest(producer='dfghjkl;')

    # Act
    products_no_filter: Page[Product] = await product_crud.get_products(db=db_fixture, params=params_no_filter)
    products_one_product: Page[Product] = await product_crud.get_products(db=db_fixture, params=params_one_product)
    products_part: Page[Product] = await product_crud.get_products(db=db_fixture, params=params_part)
    products_multiple_products: Page[Product] = await product_crud.get_products(db=db_fixture,
                                                                                params=params_multiple_products)
    products_no_results: Page[Product] = await product_crud.get_products(db=db_fixture, params=params_no_results)

    # Assert
    assert products_no_filter.total == 5
    assert products_one_product.total == 1
    assert products_one_product.items[0].producer == 'Producer 1'
    assert products_part.total == 1
    assert products_part.items[0].producer == 'Nothing'
    assert products_multiple_products.total == 3
    assert products_no_results.total == 0
