from fastapi import FastAPI

from database import engine
from repositories.accounts import SQLAccountsRepository
from repositories.tokens import SQLTokensRepository
from repositories.token_balances import SQLTokenBalancesRepository

app = FastAPI()
accounts_repository = SQLAccountsRepository(engine)
tokens_repository = SQLTokensRepository(engine)
token_balances_repository = SQLTokenBalancesRepository(engine)


from endpoints import accounts, transactions, tokens
