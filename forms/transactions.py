from pydantic import BaseModel, validator
from forms.utils import util_validate_address, util_validate_positive_integer


class TransferTransactionModel(BaseModel):
    from_account: str
    to_account: str
    value: int
    nonce: int

    @validator("from_account")
    def validate_from_account(cls, value: str) -> str:
        return util_validate_address("from_account", value)

    @validator("to_account")
    def validate_to_account(cls, value: str) -> str:
        return util_validate_address("to_account", value)

    @validator("value")
    def validate_value(cls, value: int) -> int:
        return util_validate_positive_integer("value", value)


class SupplyTransactionModel(BaseModel):
    recipient: str
    value: int

    @validator("recipient")
    def validate_recipient(cls, value: str) -> str:
        return util_validate_address("recipient", value)

    @validator("value")
    def validate_value(cls, value: int) -> int:
        return util_validate_positive_integer("value", value)


class DeployTokenForm(BaseModel):
    address: str
    name: str
    ticker: str
    total_supply: int
    owner: str
    nonce: int

    @validator("address")
    def validate_address(cls, value: str) -> str:
        return util_validate_address("address", value)

    @validator("owner")
    def validate_owner(cls, value: str) -> str:
        return util_validate_address("owner", value)

    @validator("total_supply")
    def validate_total_supply(cls, value: int) -> int:
        return util_validate_positive_integer("total_supply", value)

    @validator("nonce")
    def validate_nonce(cls, value: int) -> int:
        return util_validate_positive_integer("nonce", value)


class TransferTokenForm(BaseModel):
    token: str
    from_account: str
    to_account: str
    amount: int
    nonce: int

    @validator("token")
    def validate_token(cls, value: str) -> str:
        return util_validate_address("token", value)

    @validator("from_account")
    def validate_from_account(cls, value: str) -> str:
        return util_validate_address("from_account", value)

    @validator("to_account")
    def validate_to_account(cls, value: str) -> str:
        return util_validate_address("to_account", value)

    @validator("amount")
    def validate_amount(cls, value: int) -> int:
        return util_validate_positive_integer("amount", value)

    @validator("nonce")
    def validate_nonce(cls, value: int) -> int:
        return util_validate_positive_integer("nonce", value)
