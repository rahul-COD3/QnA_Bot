from typing import List
from fastapi import APIRouter, HTTPException
from uuid import UUID
from qna_bot.src.models.model import DataSource
from qna_bot.src.schemas.data_source_schema import CreateDataSource, DataSourceBase, UpdateDataSource
from qna_bot.src.services.data_source_service import DataSourceService

router = APIRouter(
    prefix="/api/data-source",
    tags=["data_source"],
    responses={404: {"description": "Not found"}}
)

service = DataSourceService()

@router.post("/", response_model=dict)
async def create_data_source(data_source: CreateDataSource):
    """
    Creates a new data source.

    Parameters:
    - data_source (CreateDataSource): The data source details.

    Returns:
    - Response: The result of the creation operation.
    """
    response = await service.create_data_source(data_source)
    if response.is_success:
        return {"message": response.data}
    raise HTTPException(status_code=500, detail=response.data)

@router.put("/{id}", response_model=dict)
async def update_data_source(id: UUID, data_source_update: UpdateDataSource):
    """
    Updates an existing data source.

    Parameters:
    - id (UUID): The ID of the data source to update.
    - data_source_update (UpdateDataSource): The updated details.

    Returns:
    - Response: The result of the update operation.
    """
    response = await service.update_data_source(id, data_source_update)
    if response.is_success:
        return {"message": response.data}
    raise HTTPException(status_code=404, detail=response.data)

@router.delete("/{id}", response_model=dict)
async def delete_data_source(id: UUID):
    """
    Deletes a data source by ID.

    Parameters:
    - id (UUID): The ID of the data source to delete.

    Returns:
    - Response: The result of the deletion operation.
    """
    response = await service.delete_data_source(id)
    if response.is_success:
        return {"message": response.data}
    raise HTTPException(status_code=404, detail=response.data)

# the response_model is a list of DataSource objects
@router.get("/", response_model=List[DataSourceBase])
async def get_data_sources():
    """
    Retrieves all data sources.

    Returns:
    - List[DataSource]: The list of data sources.
    """
    response = await service.get_data_sources()
    if response.is_success:
        return response.data
    raise HTTPException(status_code=500, detail=response.data)

@router.get("/{id}", response_model=DataSourceBase)
async def get_data_source(id: UUID):
    """
    Retrieves a data source by ID.

    Parameters:
    - id (UUID): The ID of the data source to retrieve.

    Returns:
    - DataSource: The requested data source.
    """
    response = await service.get_data_source(id)
    if response.is_success:
        return response.data
    raise HTTPException(status_code=404, detail=response.data)

@router.get("/by-data-space/{data_space_id}", response_model=List[DataSourceBase])
async def get_data_sources_by_data_space_id(data_space_id: UUID):
    """
    Retrieves all data sources by data space ID.

    Parameters:
    - data_space_id (UUID): The ID of the data space.

    Returns:
    - List[DataSource]: The list of data sources for the specified data space.
    """
    response = await service.get_data_sources_by_data_space_id(data_space_id)
    if response.is_success:
        return response.data
    raise HTTPException(status_code=500, detail=response.data)
