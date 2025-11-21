from fastapi import FastAPI
from backend.api.v1.endpoints import user_router, account_router, transaction_router

app = FastAPI()
app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(account_router, prefix="/accounts", tags=["accounts"])
app.include_router(transaction_router, prefix="/transactions", tags=["transactions"])

@app.get("/")
def root():
    return {"message": "Witaj w Apka Finansowa API!"}
