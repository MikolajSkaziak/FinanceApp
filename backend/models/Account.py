from sqlalchemy import Column, ForeignKey, Integer, String, Numeric,Date
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    bank_name = Column(String(50), nullable=False)
    account_name = Column(String(50), unique=True, nullable=False)
    currency = Column(String(3), nullable=False)
    balance = Column(Numeric(12,2), nullable=False)
    last_sync = Column(Date, nullable=True)
    user_id = Column(Integer,  ForeignKey("users.id"), nullable=False)
    
    user=relationship("User", back_populates="accounts")
    transactions = relationship("Transaction", back_populates="account")

    def __repr__(self):
        return f"<Account(account_name='{self.account_name}', bank_name='{self.bank_name}', balance='{self.balance}')>"