from pydantic import BaseModel, validator

from forms.utils import util_validate_address


class CreateAccountForm(BaseModel):
    address: str

    @validator("address")
    def validate_address(cls, value: str) -> str:
        return util_validate_address("address", value)


class GetNonceForm(CreateAccountForm):
    pass
