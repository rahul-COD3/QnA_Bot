import logging
from uuid import UUID
from qna_bot.src.schemas.data_source_schema import CreateDataSource, UpdateDataSource
from qna_bot.src.crud.data_source_crud import DataSourceCRUD
from qna_bot.src.models.model import DataSource
from qna_bot.src.utils.api_response import Response
from qna_bot.src.constants.messages import (
    DATA_SOURCE_CREATE_SUCCESS, DATA_SOURCE_CREATE_ERROR, DATA_SOURCE_UPDATE_SUCCESS,
    DATA_SOURCE_UPDATE_ERROR, DATA_SOURCE_DELETE_SUCCESS, DATA_SOURCE_DELETE_ERROR,
    DATA_SOURCE_NOT_FOUND, DATA_SOURCE_RETRIEVE_ERROR
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataSourceService:
    def __init__(self):
        self.crud = DataSourceCRUD()

    async def create_data_source(self, data_source: CreateDataSource) -> Response:
        try:
            data = await self.crud.create_data_source(data_source)
            return Response(data=DATA_SOURCE_CREATE_SUCCESS)
        except Exception as e:
            logger.error(f"Error creating data source: {str(e)}")
            return Response(error_message=DATA_SOURCE_CREATE_ERROR)

    async def update_data_source(self, id: UUID, data_source_update: UpdateDataSource) -> Response:
        try:
            existing_data_source = await self.crud.get_data_source(id)
            if not existing_data_source:
                return Response(error_message=DATA_SOURCE_NOT_FOUND)
            data = await self.crud.update_data_source(existing_data_source, data_source_update)
            return Response(data=DATA_SOURCE_UPDATE_SUCCESS)
        except Exception as e:
            logger.error(f"Error updating data source: {str(e)}")
            return Response(error_message=DATA_SOURCE_UPDATE_ERROR)

    async def delete_data_source(self, id: UUID) -> Response:
        try:
            data = await self.crud.delete_data_source(id)
            if not data:
                return Response(error_message=DATA_SOURCE_NOT_FOUND)
            return Response(data=DATA_SOURCE_DELETE_SUCCESS)
        except Exception as e:
            logger.error(f"Error deleting data source: {str(e)}")
            return Response(error_message=DATA_SOURCE_DELETE_ERROR)

    async def get_data_sources(self) -> Response:
        try:
            data = await self.crud.get_data_sources()
            return Response(data=data)
        except Exception as e:
            logger.error(f"Error retrieving data sources: {str(e)}")
            return Response(error_message=DATA_SOURCE_RETRIEVE_ERROR)

    async def get_data_source(self, id: UUID) -> Response:
        try:
            data = await self.crud.get_data_source(id)
            if not data:
                return Response(error_message=DATA_SOURCE_NOT_FOUND)
            return Response(data=data)
        except Exception as e:
            logger.error(f"Error retrieving data source: {str(e)}")
            return Response(error_message=DATA_SOURCE_RETRIEVE_ERROR)

    async def get_data_sources_by_data_space_id(self, data_space_id: UUID) -> Response:
        try:
            data = await self.crud.get_data_sources_by_data_space_id(data_space_id)
            return Response(data=data)
        except Exception as e:
            logger.error(f"Error retrieving data sources by data space ID: {str(e)}")
            return Response(error_message=DATA_SOURCE_RETRIEVE_ERROR)
