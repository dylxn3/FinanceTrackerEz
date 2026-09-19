from datetime import date, datetime
from decimal import Decimal
import csv
import io
import re

import pdfplumber
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.transaction import Transaction


router = APIRouter(
    prefix="/transactions",
    tags=["transactions"]
)


@router.get("/")
def get_transactions(db: Session = Depends(get_db)):
    return db.query(Transaction).all()


@router.post("/import")
async def import_transactions(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Please upload a file."
        )

    filename = file.filename.lower()

    if filename.endswith(".csv"):
        return await import_csv(file, db)

    if filename.endswith(".pdf"):
        return await import_pdf(file, db)

    raise HTTPException(
        status_code=400,
        detail="Please upload a CSV or PDF file."
    )


async def import_csv(
    file: UploadFile,
    db: Session
):
    contents = await file.read()

    try:
        text = contents.decode("utf-8-sig")
    except UnicodeDecodeError:
        raise HTTPException(
            status_code=400,
            detail="CSV must be UTF-8 encoded."
        )

    reader = csv.DictReader(io.StringIO(text))

    transactions = []

    for row in reader:
        transaction = Transaction(
            date=datetime.strptime(
                row["date"],
                "%Y-%m-%d"
            ).date(),
            description=row["description"],
            amount=Decimal(row["amount"]),
            type=row["type"],
            category=None,
            ai_confidence=None,
            categorization_source=None
        )

        db.add(transaction)
        transactions.append(transaction)

    db.commit()

    return {
        "message": "CSV imported successfully",
        "transactions_imported": len(transactions)
    }


async def import_pdf(
    file: UploadFile,
    db: Session
):
    contents = await file.read()

    parsed_transactions = []

    try:
        with pdfplumber.open(io.BytesIO(contents)) as pdf:

            for page in pdf.pages:
                words = page.extract_words(
                    x_tolerance=2,
                    y_tolerance=3
                )

                rows = group_words_into_rows(words)

                for row in rows:
                    transaction = parse_pdf_row(row)

                    if transaction:
                        parsed_transactions.append(transaction)

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Could not read PDF: {str(e)}"
        )

    for transaction_data in parsed_transactions:
        transaction = Transaction(
            date=transaction_data["date"],
            description=transaction_data["description"],
            amount=transaction_data["amount"],
            type=transaction_data["type"],
            category=None,
            ai_confidence=None,
            categorization_source=None
        )

        db.add(transaction)

    db.commit()

    return {
        "message": "PDF imported successfully",
        "transactions_imported": len(parsed_transactions),
        "transactions": parsed_transactions
    }


def group_words_into_rows(words):
    rows = []

    for word in words:
        top = round(word["top"], 1)

        matching_row = None

        for row in rows:
            if abs(row["top"] - top) <= 3:
                matching_row = row
                break

        if matching_row:
            matching_row["words"].append(word)
        else:
            rows.append({
                "top": top,
                "words": [word]
            })

    for row in rows:
        row["words"].sort(key=lambda word: word["x0"])

    rows.sort(key=lambda row: row["top"])

    return rows


def parse_pdf_row(row):
    text = " ".join(
        word["text"]
        for word in row["words"]
    )

    date_match = re.search(
        r"\b(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)\d{2}\b",
        text,
        re.IGNORECASE
    )

    if not date_match:
        return None

    money_matches = re.findall(
        r"\b\d+\.\d{2}\b",
        text
    )

    if not money_matches:
        return None

    amount = Decimal(money_matches[0])

    date_text = date_match.group(0).upper()

    month = date_text[:3]
    day = int(date_text[3:])

    month_number = {
        "JAN": 1,
        "FEB": 2,
        "MAR": 3,
        "APR": 4,
        "MAY": 5,
        "JUN": 6,
        "JUL": 7,
        "AUG": 8,
        "SEP": 9,
        "OCT": 10,
        "NOV": 11,
        "DEC": 12
    }[month]

    transaction_date = date(
        2026,
        month_number,
        day
    )

    description = text.replace(
        date_match.group(0),
        ""
    ).strip()

    return {
        "date": transaction_date,
        "description": description,
        "amount": amount,
        "type": "debit"
    }