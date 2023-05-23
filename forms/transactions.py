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
