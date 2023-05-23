from main import app, accounts_repository
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
        raise ValueError("Sender has no enough balance")
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
