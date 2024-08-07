from pydantic import BaseModel
from qna_bot.src.models.model import DataSourceType
from uuid import UUID

# define a enum for data source type


class CreateDataSource(BaseModel):
    type: DataSourceType
    location: str
    is_auth_required: bool
    data_space_id: UUID

class UpdateDataSource(BaseModel):
    type: DataSourceType
    location: str
    is_auth_required: bool

class DataSourceBase(BaseModel):
    id: UUID
    type: DataSourceType
    location: str
    is_auth_required: bool
    data_space_id: UUID

    class Config:
        from_attributes = True