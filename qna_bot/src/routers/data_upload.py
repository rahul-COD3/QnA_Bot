from msilib.schema import File
from fastapi import FastAPI, UploadFile

app = FastAPI()

@app.upload("/upload")
def upload_file(file: UploadFile = File(...)):
    print(file)
    return {"filename": file.filename}