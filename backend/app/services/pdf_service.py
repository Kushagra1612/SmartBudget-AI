import logging
import os

from fastapi import HTTPException

from app.parsers.bank_parser import BankStatementParser

logger = logging.getLogger(__name__)


class PDFService:

    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

    @staticmethod
    def parse_statement(filepath: str):

        # File existence
        if not os.path.exists(filepath):
            raise HTTPException(
                status_code=404,
                detail="Uploaded file not found.",
            )

        # File type
        if not filepath.lower().endswith(".pdf"):
            raise HTTPException(
                status_code=400,
                detail="Only PDF files are supported.",
            )

        # File size
        file_size = os.path.getsize(filepath)

        if file_size == 0:
            raise HTTPException(
                status_code=400,
                detail="Uploaded PDF is empty.",
            )

        if file_size > PDFService.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail="PDF exceeds the maximum allowed size (10 MB).",
            )

        try:
            result = BankStatementParser.parse(filepath)

            if result is None:
                raise HTTPException(
                    status_code=422,
                    detail="Unable to parse bank statement.",
                )

            if (
                "transactions" not in result
                or not isinstance(result["transactions"], list)
            ):
                raise HTTPException(
                    status_code=422,
                    detail="Invalid parser response.",
                )

            logger.info(
                "Successfully parsed %d transactions using %s",
                len(result["transactions"]),
                result.get("method", "unknown"),
            )

            return result

        except HTTPException:
            raise

        except Exception:
            logger.exception(
                "Unexpected error while parsing PDF: %s",
                filepath,
            )

            raise HTTPException(
                status_code=500,
                detail="An unexpected error occurred while parsing the PDF.",
            )