from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models.transaction import Transaction
from app.api.transactions import router as transactions_router


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Finance Tracker")

app.include_router(transactions_router)


@app.get("/")
def root():
    return {"message": "Finance Tracker API is running"}


@app.get("/health/db")
def database_health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))

    return {"database": "connected"}