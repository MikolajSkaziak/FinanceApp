from backend.db import SessionLocal
from backend.crud import user_crud, account_crud, transaction_crud
from backend.models.Transaction import Transaction
from backend.models.Account import Account
from backend.models.User import User

def test_cruds():
    db = SessionLocal()

    try:
        # ----- CZYSZCZENIE TESTOWYCH DANYCH -----
        db.query(Transaction).delete()  
        db.query(Account).delete()     
        db.query(User).delete()        
        db.commit()

        # ----- TEST USER -----
        user = user_crud.create_user(db, username="testuser", email="test@example.com", password_hash="tajne")
        print("Dodany użytkownik:", user)

        users = user_crud.get_users(db)
        print("Wszyscy użytkownicy:", users)

        # ----- TEST ACCOUNT -----
        account = account_crud.create_account(
            db=db,
            bank_name="TestBank",
            account_name="testkonto",
            currency="PLN",
            balance=1000,
            user_id=user.id
        )
        print("Dodane konto:", account)

        accounts = account_crud.get_accounts(db)
        print("Wszystkie konta:", accounts)

        # ----- TEST TRANSACTION -----
        transaction = transaction_crud.create_transaction(
            db=db,
            amount=500,
            currency="PLN",
            transaction_type="INCOME",
            account_id=account.id
        )
        print("Dodana transakcja:", transaction)

        transactions = transaction_crud.get_transactions(db)
        print("Wszystkie transakcje:", transactions)

        # ----- TEST DELETE -----
        db.query(Transaction).filter(Transaction.account_id == account.id).delete()
        db.commit()

        account_crud.delete_account(db, account.id)
        user_crud.delete_user(db, user.id)
        print("Usuń testowe dane zakończony")

    finally:
        db.close()


if __name__ == "__main__":
    test_cruds()
