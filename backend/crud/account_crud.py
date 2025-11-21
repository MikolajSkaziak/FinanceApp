from backend.db import get_db
from backend.models.Account import Account
from sqlalchemy.orm import Session
def create_account(db: Session, bank_name: str, account_name: str, currency: str, balance: float, user_id: int):
    account = Account(
        bank_name=bank_name,
        account_name=account_name,
        currency=currency,
        balance=balance,
        user_id=user_id
    )
    db.add(account)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    db.refresh(account)
    return account

def get_accounts(db: Session):
    return db.query(Account).all()

def delete_account(db: Session, account_id: int):
    account = db.query(Account).filter(Account.id == account_id).first()
    if account:
        db.delete(account)
        db.commit()
        return True
    return False

def get_account_by_id(db: Session, account_id: int):
    return db.query(Account).filter(Account.id == account_id).first()