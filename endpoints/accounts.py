from typing import Dict

from forms.accounts import CreateAccountForm
from main import accounts_repository
from main import app


@app.post("/accounts/")
async def create_account(form: CreateAccountForm):
    already_existing_account = accounts_repository.get(address=form.address)
    if already_existing_account:
        return {"error": "already exists"}
    accounts_repository.create_empty_account(form.address)
    return {"address": form.address}


@app.get("/accounts/")
async def get_accounts() -> Dict:
    values = accounts_repository.list()
    return {
        "size": len(values),
        "data": values
    }


@app.get("/nonce/{address}")
async def get_nonce(address: str) -> Dict:
    if not (account := accounts_repository.get(address)):
        return {"error": "account does not exist"}
    return {"nonce": account.nonce}


@app.get("/balance/{address}")
async def get_balance(address: str) -> Dict:
    if not (account := accounts_repository.get(address)):
        return {"error": "account does not exist"}
    return {"balance": account.balance}
