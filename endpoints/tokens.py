from typing import Dict

from main import app, tokens_repository, token_balances_repository


@app.get("/tokens/{token_address}/balance_of/{account_address}")
async def balance_of(token_address: str, account_address: str) -> Dict:
    if not tokens_repository.get_by_address(address=token_address):
        return {"error": "bad token address"}
    if not (balance := token_balances_repository.get_by_holder_and_token(holder=account_address, token=token_address)):
        balance = 0
    else:
        balance = balance.amount
    return {
        "token": token_address,
        "account": account_address,
        "balance": balance
    }


@app.get("/tokens/get_by_address/{address}")
async def get_token_by_address(address: str):
    if not (token := tokens_repository.get_by_address(address)):
        return {"error": "no token found"}
    else:
        return token


@app.get("/tokens/get_by_name/{name}")
async def get_token_by_name(name: str):
    if not (token := tokens_repository.get_by_name(name)):
        return {"error": "no token found"}
    else:
        return token


@app.get("/tokens/get_by_ticker/{ticker}")
async def get_token_by_ticker(ticker: str):
    if not (token := tokens_repository.get_by_ticker(ticker)):
        return {"error": "no token found"}
    else:
        return token
