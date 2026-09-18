import csv
import io
from datetime import date
from decimal import Decimal

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.transaction import Transaction


router = APIRouter(
    prefix="/transactions",
    tags=["transactions"]
)


@router.post("/import")
async def import_transactions(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Make sure the uploaded file is a CSV
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Please upload a CSV file."
        )

    # Read the file
    contents = await file.read()

    try:
        text = contents.decode("utf-8-sig")
    except UnicodeDecodeError:
        raise HTTPException(
            status_code=400,
            detail="CSV file must use UTF-8 encoding."
        )

    # Turn the CSV into rows
    reader = csv.DictReader(io.StringIO(text))

    # Make sure the required columns exist
    required_columns = {
        "date",
        "description",
        "amount",
        "type"
    }

    if not reader.fieldnames:
        raise HTTPException(
            status_code=400,
            detail="CSV file is empty."
        )

    missing_columns = required_columns - set(reader.fieldnames)

    if missing_columns:
        raise HTTPException(
            status_code=400,
            detail=f"Missing columns: {', '.join(missing_columns)}"
        )

    transactions = []

    for row_number, row in enumerate(reader, start=2):
        try:
            transaction_date = date.fromisoformat(
                row["date"].strip()
            )

            description = row["description"].strip()

            amount = Decimal(
                row["amount"].strip()
            )

            transaction_type = row["type"].strip().lower()

        except (ValueError, TypeError):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid data on row {row_number}."
            )

        if not description:
            raise HTTPException(
                status_code=400,
                detail=f"Missing description on row {row_number}."
            )

        if transaction_type not in {"debit", "credit"}:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Invalid transaction type on row {row_number}. "
                    "Expected 'debit' or 'credit'."
                )
            )

        transaction = Transaction(
            date=transaction_date,
            description=description,
            amount=amount,
            type=transaction_type,
        )

        transactions.append(transaction)

    # Save all transactions
    db.add_all(transactions)
    db.commit()

    return {
        "message": "Transactions imported successfully.",
        "count": len(transactions)
    }