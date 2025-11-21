from fastapi import FastAPI
from backend.api.v1.auth import router as auth_router
from backend.api.v1.endpoints.users import router as user_router
from backend.api.v1.endpoints.accounts import router as account_router
from backend.api.v1.endpoints.transactions import router as transaction_router

app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(account_router, prefix="/accounts", tags=["accounts"])
app.include_router(transaction_router, prefix="/transactions", tags=["transactions"])

@app.get("/")
def root():
    return {"message": "Witaj w Apka Finansowa API!"}
