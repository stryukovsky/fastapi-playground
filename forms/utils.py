from web3 import Web3


def util_validate_address(field_name: str, value: str) -> str:
    try:
        return Web3.to_checksum_address(value)
    except Exception:
        raise ValueError(f"Bad address {field_name}: {value}")


def util_validate_positive_integer(field_name: str, value: int) -> int:
    if value < 0:
        raise ValueError(f"Bad positive integer {field_name}: {value}")
    return value
