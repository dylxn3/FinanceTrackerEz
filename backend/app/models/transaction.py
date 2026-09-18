from datetime import date, datetime
from decimal import Decimal
from sqlalchemy import Date, DateTime, Float, Integer, String, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    date: Mapped[date] = mapped_column(Date, nullable=False)

    description: Mapped[str] = mapped_column(String(255), nullable=False)

    amount: Mapped[Decimal] = mapped_column(
    Numeric(12, 2),
    nullable=False)
    
    type: Mapped[str] = mapped_column(String(20), nullable=False)

    category: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    ai_confidence: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    categorization_source: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )