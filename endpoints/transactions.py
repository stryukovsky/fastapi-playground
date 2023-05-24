from typing import Dict

from forms.tokens import DeployTokenForm, TransferTokenForm
from main import app, accounts_repository, tokens_repository, token_balances_repository
from forms.transactions import TransferTransactionModel, SupplyTransactionModel


@app.post("/transact")
async def transact(transaction: TransferTransactionModel):
    from_account = accounts_repository.get(address=transaction.from_account)
    if not from_account:
        return {"error": "Sender has no initialized account yet"}
    to_account = accounts_repository.get(address=transaction.to_account)
    if transaction.nonce != from_account.nonce + 1:
        return {"error": "Bad nonce"}
    if not to_account:
        accounts_repository.create_empty_account(address=transaction.to_account)
        to_account = accounts_repository.get(address=transaction.to_account)
    if from_account.balance < transaction.value:
        return {"error": "Sender has no enough balance"}
    from_account.balance -= transaction.value
    to_account.balance += transaction.value
    from_account.nonce += 1
    accounts_repository.apply_transaction([from_account, to_account])
    return {
        "status": "success"
    }


@app.post("/supply")
async def supply_account(supply_transaction: SupplyTransactionModel):
    recipient_account = accounts_repository.get(address=supply_transaction.recipient)
    if not recipient_account:
        accounts_repository.create_empty_account(address=supply_transaction.recipient)
        recipient_account = accounts_repository.get(address=supply_transaction.recipient)
    recipient_account.balance += supply_transaction.value
    accounts_repository.apply_transaction([recipient_account])
    return {
        "status": "success"
    }


@app.post("/tokens/deploy")
async def deploy(form: DeployTokenForm) -> Dict:
    if not (owner := accounts_repository.get(form.owner)):
        return {"error": "no token owner"}
    if form.nonce != owner.nonce + 1:
        return {"error": "bad nonce"}
    if accounts_repository.get(form.address):
        return {"error": "address already used by some EOA"}
    if tokens_repository.get_by_address(form.address):
        return {"error": "address already used by some token"}
    if tokens_repository.get_by_name(form.name):
        return {"error": "name already used by some token"}
    if tokens_repository.get_by_ticker(form.ticker):
        return {"error": "ticker already used by some token"}
    owner.nonce += 1
    tokens_repository.deploy_token(owner, form.address, form.name, form.ticker, form.total_supply)
    return {"status": "success"}


@app.post("/tokens/transfer")
async def transfer(form: TransferTokenForm) -> Dict:
    if not (sender := accounts_repository.get(address=form.from_account)):
        return {"error": "bad sender"}
    if form.nonce != sender.nonce + 1:
        return {"error": "bad nonce"}
    if not (from_account_balance := token_balances_repository.get_by_holder_and_token(form.from_account, form.token)):
        return {"error": "no from account found"}
    if from_account_balance.amount < form.amount:
        return {"error": "insufficient balance"}
    if not (to_account_balance := token_balances_repository.get_by_holder_and_token(form.to_account, form.token)):
        token_balances_repository.create(form.token, form.to_account)
        to_account_balance = token_balances_repository.get_by_holder_and_token(form.to_account, form.token)
    sender.nonce += 1
    to_account_balance.amount += form.amount
    from_account_balance.amount -= form.amount
    token_balances_repository.apply_transfer_transaction(sender, from_account_balance, to_account_balance)
    return {"status": "success"}
