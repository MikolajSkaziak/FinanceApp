from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.db import get_db
from backend.crud import account_crud
from pydantic import BaseModel

router = APIRouter()

# Walidacje danych
class AccountCreate(BaseModel):
    bank_name: str
    account_name: str
    currency: str
    balance: float
    user_id: int

# POST accounts
@router.post("/", response_model=dict)
def create_account(account: AccountCreate, db: Session = Depends(get_db)):
    db_account = account_crud.create_account(db, **account.dict())
    return {"id": db_account.id, "bank_name": db_account.bank_name, "account_name": db_account.account_name, "currency": db_account.currency, "balance": db_account.balance, "user_id": db_account.user_id}

# GET accounts
@router.get("/", response_model=list[dict])
def list_accounts(db: Session = Depends(get_db)):
    accounts = account_crud.get_accounts(db)
    return [{"id": a.id, "bank_name": a.bank_name, "account_name": a.account_name, "currency": a.currency, "balance": a.balance, "user_id": a.user_id} for a in accounts]