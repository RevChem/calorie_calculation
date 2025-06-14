from datetime import datetime
from typing import Annotated, List
from config import settings
from sqlalchemy import Integer, func, Text, String, ARRAY
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column, class_mapper
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine


DATABASE_URL = settings.get_db_url()

engine = create_async_engine(url = DATABASE_URL)

class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key = True, autoincrement = True)
    created_at: Mapped[datetime] = mapped_column(server_default = func.now())
    updated_up: Mapped[datetime] = mapped_column(server_default = func.now())

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + 's'
    
    def to_dict(self) -> dict:
        columns = class_mapper(self.__class__).columns
        return {column.key: getattr(self, column.key) for column in columns}
    