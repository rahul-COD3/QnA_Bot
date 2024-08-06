import os
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
from qna_bot.src.constants.document_upload import FILE_UPLOAD_SUCCESS, FILE_UPLOAD_ERROR
from qna_bot.src.utils.api_response import Response
from dotenv import load_dotenv
import logging
import uuid

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AzureBlobUploader:
    def __init__(self, storage_url: str = None, credential=None):
        """
        Initializes the AzureBlobUploader with optional storage URL and credential.

        :param storage_url: Azure Storage Blob URL.
        :param credential: Azure credential object (default: DefaultAzureCredential).
        """
        self.storage_url = storage_url or os.getenv("AZURE_STORAGE_BLOB_URL")
        self.container_name = os.getenv("AZURE_STORAGE_BLOB_CONTAINER_NAME")
        self.credential = credential or DefaultAzureCredential()
        self.blob_service_client = BlobServiceClient(account_url=self.storage_url, credential=self.credential)

    async def upload_blob(self, file) -> str:
        """
        Uploads data to an Azure Blob Storage container.
        :param file: File-like object to be uploaded.
        :return: Message indicating the result of the upload operation.
        """
        try:
            # Read file content
            data = await file.read()
            blob_name = str(uuid.uuid4()) + "_" + file.filename
            container_client = self.blob_service_client.get_container_client(self.container_name)
            blob_client = container_client.get_blob_client(blob_name)

            # Convert data to bytes if it's a string
            if isinstance(data, str):
                data = data.encode('utf-8')

            # Upload the blob
            blob_client.upload_blob(data, overwrite=True)
            logger.info(f"Blob uploaded successfully: {blob_name}")
            return Response(data=FILE_UPLOAD_SUCCESS)

        except Exception as e:
            logger.error(f"An unexpected error occurred: {str(e)}")
            return Response(error_message=FILE_UPLOAD_ERROR)
