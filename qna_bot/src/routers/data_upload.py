from fastapi import APIRouter, File, UploadFile, HTTPException
from qna_bot.src.services.azure_blob_service import AzureBlobUploader

router = APIRouter(
    prefix = "/api/document",
    tags=["document"],
    responses={404: {"description": "Not found"}}
)

# Initialize the Azure Blob Uploader
blob_uploader = AzureBlobUploader()

@router.post("/upload/",)
async def upload_file(file: UploadFile = File(...)):
    """
    Uploads a file to the server.

    Parameters:
    - file (UploadFile): The file to be uploaded.

    Returns:
    - result: The result of the file upload.
    """
    result = await blob_uploader.upload_blob(file)
    if result.is_success:
        return {"message": result.data}
    else:
        raise HTTPException(status_code=500, detail=result.data)