import os
import shutil

from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.services.pdf_service import PDFService
from app.schemas.upload import UploadResponse

router = APIRouter(
    prefix="/upload",
    tags=["Upload"],
)

UPLOAD_DIR = "app/uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post(
    "/statement",
    response_model=UploadResponse,
)
async def upload_statement(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    filepath = os.path.join(
        UPLOAD_DIR,
        file.filename,
    )

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = PDFService.parse_statement(filepath)

    return {
    "filename": file.filename,
    "transactions_found": len(result["transactions"]),
    "message": "Statement parsed successfully.",
    "method": result["method"],
    "transactions": result["transactions"],
}