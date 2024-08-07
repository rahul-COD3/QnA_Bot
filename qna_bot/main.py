from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from qna_bot.src.config.seed_data import SeedData
from contextlib import asynccontextmanager
from qna_bot.src.services.azure_blob_service import AzureBlobUploader
from qna_bot.src.routers import data_source_routes, data_upload_routes


@asynccontextmanager
async def lifespan(app: FastAPI):
    seed_data = SeedData()
    await seed_data.seed()

    yield
    seed_data.clear()

app = FastAPI(lifespan=lifespan)
app.include_router(data_upload_routes.router)
app.include_router(data_source_routes.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

# Initialize the Azure Blob Uploader
blob_uploader = AzureBlobUploader()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)


