from enum import Enum
from sqlalchemy import Column, ForeignKey, Integer, Numeric, String, DateTime
from sqlalchemy.orm import declarative_base,relationship
from datetime import datetime
from backend.models.enums import TransactionType

Base= declarative_base()

class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    amount = Column(Numeric(12,2), nullable=False)
    currency = Column(String(3), nullable=False)
    transaction_type = Column(Enum(TransactionType), nullable=False)
    category = Column(String(50), nullable=True)
    date = Column(DateTime, default=datetime.utcnow, nullable=False)
    description = Column(String(200), nullable=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)

    account = relationship("Account", back_populates="transactions")

    def __repr__(self):
        return f"<Transaction(amount={self.amount}, type={self.transaction_type}, date={self.date})>"