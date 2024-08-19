import asyncio

import pandas
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import product_crud
from app.db.postgres import SessionLocal
from app.schemas.product import ProductCreate

_csv_file_path = 'data.csv'


async def _update_products_from_csv(db: AsyncSession, file_path: str):
    df = pandas.read_csv(file_path)
    print(df.keys())

    create_data: list[ProductCreate] = []
    for _, row in df.iterrows():
        create_data.append(ProductCreate(id=row['sku (unique id)'],
                                         name=row['product_name'],
                                         photo_url=row['photo_url'] if not pandas.isna(row['photo_url']) else None,
                                         barcode=row['barcode'],
                                         price_cents=row['price_cents'],
                                         producer=row['producer'] if not pandas.isna(row['producer']) else None))

    await product_crud.upsert_products(db=db, create_data=create_data)


async def main():
    session = SessionLocal()

    await _update_products_from_csv(db=session, file_path=_csv_file_path)

    await session.commit()
    await session.close()


if __name__ == '__main__':
    asyncio.run(main())
