"""
Integration tests for POST /upload/statement.

PDFService.parse_statement is mocked here -- it does real PDF table
extraction (pdfplumber/camelot) tuned against real bank statement
layouts. A fabricated test PDF wouldn't exercise that logic honestly, it
would just test against whatever fake format I invented. What IS tested
end to end for real: file validation, statement + transaction creation
from a parsed result, and error handling -- the router's own logic,
which is what these tests are actually responsible for.

Real-PDF parser accuracy is a separate concern from parsers/bank_parser.py
etc. -- not covered here.
"""

import io

from datetime import date
from unittest.mock import patch


def _fake_parsed_result():
    return {
        "bank": "Test Bank",
        "method": "pdfplumber",
        "pages": 1,
        "confidence": 0.95,
        "transactions": [
            {
                "date": date(2026, 8, 1),
                "debit": "500",
                "credit": "0",
                "balance": "10000",
                "category": "Food",
                "merchant": "Test Merchant",
                "description": "Groceries",
                "payment_mode": "UPI",
                "transaction_type": "Expense",
            },
        ],
    }


def test_requires_authentication(client):
    response = client.post(
        "/upload/statement",
        files={"file": ("statement.pdf", b"%PDF-1.4 fake", "application/pdf")},
    )
    assert response.status_code == 401


def test_rejects_a_non_pdf_file(client, auth_headers):
    response = client.post(
        "/upload/statement",
        files={"file": ("statement.txt", b"not a pdf", "text/plain")},
        headers=auth_headers,
    )
    assert response.status_code == 400


def test_rejects_an_empty_file(client, auth_headers):
    response = client.post(
        "/upload/statement",
        files={"file": ("statement.pdf", b"", "application/pdf")},
        headers=auth_headers,
    )
    assert response.status_code == 400


def test_uploads_and_saves_a_parsed_statement(client, auth_headers):
    with patch(
        "app.routers.upload.PDFService.parse_statement",
        return_value=_fake_parsed_result(),
    ):
        response = client.post(
            "/upload/statement",
            files={
                "file": (
                    "statement.pdf",
                    io.BytesIO(b"%PDF-1.4 fake pdf bytes").read(),
                    "application/pdf",
                )
            },
            headers=auth_headers,
        )

    assert response.status_code == 200
    body = response.json()
    assert body["bank"] == "Test Bank"
    assert body["transactions_found"] == 1


def test_rejects_a_statement_with_no_transactions_found(client, auth_headers):
    empty_result = _fake_parsed_result()
    empty_result["transactions"] = []

    with patch(
        "app.routers.upload.PDFService.parse_statement",
        return_value=empty_result,
    ):
        response = client.post(
            "/upload/statement",
            files={
                "file": ("statement.pdf", b"%PDF-1.4 fake pdf bytes", "application/pdf")
            },
            headers=auth_headers,
        )

    assert response.status_code == 422


def test_uploaded_transactions_then_appear_in_the_transactions_list(
    client, auth_headers
):
    with patch(
        "app.routers.upload.PDFService.parse_statement",
        return_value=_fake_parsed_result(),
    ):
        client.post(
            "/upload/statement",
            files={
                "file": ("statement.pdf", b"%PDF-1.4 fake pdf bytes", "application/pdf")
            },
            headers=auth_headers,
        )

    response = client.get("/transactions", headers=auth_headers)

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["merchant"] == "Test Merchant"
