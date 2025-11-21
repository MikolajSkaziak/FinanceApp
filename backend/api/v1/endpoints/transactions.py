from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.db import get_db
from backend.crud import transaction_crud
from pydantic import BaseModel

router = APIRouter()

# Walidacje danych
class TransactionCreate(BaseModel):
    amount: float
    currency: str
    transaction_type: str
    account_id: int

# POST transactions
@router.post("/", response_model=dict)
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    db_transaction = transaction_crud.create_transaction(db, **transaction.dict())
    return {"id": db_transaction.id, "amount": db_transaction.amount, "currency": db_transaction.currency, "transaction_type": db_transaction.transaction_type, "account_id": db_transaction.account_id}

# GET transactions
@router.get("/", response_model=list[dict])
def list_transactions(db: Session = Depends(get_db)):
    transactions = transaction_crud.get_transactions(db)
    return [{"id": t.id, "amount": t.amount, "currency": t.currency, "transaction_type": t.transaction_type, "account_id": t.account_id} for t in transactions]