from typing import Annotated, List
from dao.database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sql_enums import Gender, FoodCalories


uniq_str = Annotated[str, mapped_column(unique = True)]


class User(Base):
    username: Mapped[uniq_str]
    email: Mapped[uniq_str]
    password: Mapped[str]

    profile: Mapped['Profile'] = relationship(
        back_populates = 'user',
        uselist = False,
        lazy = 'joined'
    )

    food_entrie: Mapped[List['Food_entrie']] = relationship(
        back_populates = 'user',
        lazy = 'dynamic'  # Ленивая загрузка + возможность применения кастомного фильтра
    )


class Profile(Base):
    first_name: Mapped[str]
    last_name: Mapped[str | None]
    age: Mapped[int | None]
    gender: Mapped[Gender]
    weight: Mapped[int | None]
    height: Mapped[int | None]

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), unique=True)

    user: Mapped['User'] = relationship(
        back_populates = 'profile',
        uselist = False
    )


class Food_entrie(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    food_type: Mapped[FoodCalories]
    calories: Mapped[int]
    portion_size: Mapped[float]
    
    user: Mapped['User'] = relationship(back_populates = 'food_entrie')

