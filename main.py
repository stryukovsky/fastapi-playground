from fastapi import FastAPI

from database import engine
from repositories.accounts import SQLAccountsRepository

app = FastAPI()
accounts_repository = SQLAccountsRepository(engine)


from endpoints import accounts, transactions
