from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from qna_bot.src.config.db import AsyncSessionLocal
from qna_bot.src.schemas.data_source_schema import CreateDataSource, UpdateDataSource
from qna_bot.src.models.model import DataSource

class DataSourceCRUD:
    def __init__(self):
        self.db = AsyncSessionLocal()

    async def create_data_source(self, data_source: CreateDataSource):
        db_data_source = DataSource(**data_source.model_dump())
        self.db.add(db_data_source)
        await self.db.commit()
        await self.db.refresh(db_data_source)
        return db_data_source

    async def update_data_source(self, data_source: DataSource, data_source_update: UpdateDataSource):
        for key, value in data_source_update.model_dump().items():
            setattr(data_source, key, value)
        await self.db.commit()
        await self.db.refresh(data_source)
        return data_source

    async def delete_data_source(self, id: UUID):
        db_data_source = await self.db.get(DataSource, id)
        if db_data_source:
            await self.db.delete(db_data_source)
            await self.db.commit()
        return db_data_source

    async def get_data_sources(self):
        result = await self.db.execute(select(DataSource))
        return result.scalars().all()

    async def get_data_source(self, id: UUID):
        result = await self.db.execute(select(DataSource).filter(DataSource.id == id))
        return result.scalar_one_or_none()

    async def get_data_sources_by_data_space_id(self, data_space_id: UUID):
        result = await self.db.execute(select(DataSource).filter(DataSource.data_space_id == data_space_id))
        return result.scalars().all()
