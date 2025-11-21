from backend.db import get_db
from backend.models.Transaction import Transaction
from sqlalchemy.orm import Session 
def create_transaction(db: Session, amount: float, currency: str, transaction_type: str, account_id: int):
    transaction = Transaction(
        amount=amount,
        currency=currency,
        transaction_type=transaction_type,
        account_id=account_id
    )
    db.add(transaction)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    db.refresh(transaction)
    return transaction

def get_transactions(db: Session):

    return db.query(Transaction).all()

def get_transaction_by_id(db: Session, transaction_id: int):
    return db.query(Transaction).filter(Transaction.id == transaction_id).first()