from sqlalchemy import UUID, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Type, TypeVar
from pydantic import BaseModel
from sqlalchemy.orm import declarative_base


Schema = TypeVar("Schema", bound=BaseModel, covariant=True)
Model = TypeVar("Model", bound=declarative_base())


class BaseCrud:

    base_model: Model
    update_schema: Type[Schema]
    create_schema: Type[Schema]
    get_schema: Type[Schema]

    @classmethod
    async def get_all(cls, session: AsyncSession) -> List[Schema]:
        result = await session.execute(select(cls.base_model))
        obj = result.scalars().all()
        return [cls.get_schema.model_validate(item) for item in obj]

    @classmethod
    async def get_by_id(cls, session: AsyncSession, id: UUID | int) -> Schema | None:
        result = await session.execute(
            select(cls.base_model).where(cls.base_model.id == id)
        )
        obj = result.scalar_one_or_none()
        return cls.get_schema.model_validate(obj)

    @classmethod
    async def get_filtered_by_param(
        cls, session: AsyncSession, **kwargs
    ) -> Schema | None:

        result = await session.execute(select(cls.base_model).filter_by(**kwargs))
        obj = result.scalars().all()
        return [cls.get_schema.model_validate(item) for item in obj]

    @classmethod
    async def get_obj_by_param(cls, session: AsyncSession, **kwargs) -> Schema | None:
        result = await session.execute(select(cls.base_model).filter_by(**kwargs))
        obj = result.scalars().first()
        return cls.get_schema.model_validate(obj) if obj else None

    @classmethod
    async def create(cls, session: AsyncSession, **kwargs) -> Schema:
        instance = cls.base_model(**kwargs)
        session.add(instance)
        await session.commit()
        await session.refresh(instance)
        return cls.get_schema.model_validate(instance)

    @classmethod
    async def update(
        cls, session: AsyncSession, record_id: UUID | int, **kwargs
    ) -> Schema:

        clean_kwargs = {
            key: value for key, value in kwargs.items() if value is not None
        }
        await session.execute(
            update(cls.base_model)
            .where(cls.base_model.id == record_id)
            .values(**clean_kwargs)
        )
        await session.commit()
        instance = await cls.get_by_id(session, id=record_id)
        return cls.get_schema.model_validate(instance)

    @classmethod
    async def delete(cls, session: AsyncSession, record_id: UUID | int):

        await session.execute(
            delete(cls.base_model).where(cls.base_model.id == record_id)
        )
        await session.commit()