from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, func, Integer, String, UUID as BD_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Product(Base):
    __tablename__ = 'products'

    id: Mapped[UUID] = mapped_column(BD_UUID, primary_key=True)  # noqa: A003
    name: Mapped[str | None] = mapped_column(String(256), nullable=False, index=True)
    photo_url: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    barcode: Mapped[str] = mapped_column(String(24), nullable=False)
    price_cents: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    producer: Mapped[str] = mapped_column(String(256), nullable=True, index=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime,
                                                 server_default=func.now(),
                                                 onupdate=func.now(),
                                                 nullable=False)
