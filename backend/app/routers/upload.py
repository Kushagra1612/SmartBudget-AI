import logging
import os
import shutil
import uuid

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
)
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.upload import UploadResponse
from app.services.pdf_service import PDFService
from app.services.statement_service import StatementService
from app.services.transaction_service import TransactionService

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/upload",
    tags=["Upload"],
)

UPLOAD_DIR = "app/uploads"
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post(
    "/statement",
    response_model=UploadResponse,
)
async def upload_statement(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    # Validate extension
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed.",
        )

    contents = await file.read()

    if len(contents) == 0:
        raise HTTPException(
            status_code=400,
            detail="Uploaded PDF is empty.",
        )

    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="PDF exceeds the maximum allowed size (10 MB).",
        )

    file.file.seek(0)

    unique_filename = f"{uuid.uuid4()}.pdf"

    filepath = os.path.join(
        UPLOAD_DIR,
        unique_filename,
    )

    try:

        # Save uploaded PDF
        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        logger.info(
            "User %s uploaded %s",
            current_user.id,
            file.filename,
        )

        # Parse statement
        result = PDFService.parse_statement(filepath)

        transactions = result.get("transactions", [])

        if not transactions:
            raise HTTPException(
                status_code=422,
                detail="No transactions found in statement.",
            )

        # Get statement month/year from first transaction
        statement_date = transactions[0]["date"]

        statement_month = statement_date.month
        statement_year = statement_date.year

        # Save statement
        statement = StatementService.create_statement(
            db=db,
            user_id=current_user.id,
            filename=unique_filename,
            original_filename=file.filename,
            bank=result.get("bank", "Unknown"),
            parser_method=result.get("method", "Unknown"),
            pages=result.get("pages", 1),
            confidence=result.get("confidence", 1.0),
            month=statement_month,
            year=statement_year,
        )

        logger.info(
            "Created statement %s for user %s",
            statement.id,
            current_user.id,
        )

        # Save transactions
        saved_transactions = TransactionService.save_transactions(
            db=db,
            user_id=current_user.id,
            statement_id=statement.id,
            parsed_transactions=transactions,
        )

        logger.info(
            "Saved %d transactions for statement %s",
            len(saved_transactions),
            statement.id,
        )

        return {
            "statement_id": str(statement.id),
            "filename": file.filename,
            "bank": statement.bank,
            "pages": statement.pages,
            "confidence": statement.confidence,
            "transactions_found": len(saved_transactions),
            "message": "Statement uploaded successfully.",
            "method": statement.parser_method,
            "transactions": transactions,
        }

    except HTTPException:
        raise

    except Exception as e:

        logger.exception(
            "Statement upload failed for user %s",
            current_user.id,
        )

        raise HTTPException(
            status_code=500,
            detail=f"Upload failed: {str(e)}",
        )

    finally:

        if os.path.exists(filepath):

            try:

                os.remove(filepath)

                logger.info(
                    "Temporary file deleted: %s",
                    filepath,
                )

            except Exception:

                logger.warning(
                    "Failed to delete temporary file: %s",
                    filepath,
                )