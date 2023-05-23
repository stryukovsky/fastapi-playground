import abc
from typing import List, Optional
from sqlalchemy import Engine, Row
from sqlalchemy.orm import Session
from sqlalchemy import select, update

from database import Account


class AccountsRepository(abc.ABC):

    @abc.abstractmethod
    def save(self, account: Account):
        pass

    @abc.abstractmethod
    def apply_transaction(self, accounts: List[Account]):
        pass

    @abc.abstractmethod
    def create_empty_account(self, address: str):
        pass

    @abc.abstractmethod
    def get(self, address: str) -> Account:
        pass

    @abc.abstractmethod
    def list(self) -> List[Account]:
        pass


class SQLAccountsRepository:
    engine: Engine

    def __init__(self, engine: Engine):
        self.engine = engine

    def save(self, account: Account):
        with Session(self.engine) as session:
            session.add(account)
            session.commit()

    def create_empty_account(self, address: str):
        with Session(self.engine) as session:
            session.add(Account(address=address))
            session.commit()

    def apply_transaction(self, accounts: List[Account]):
        with self.engine.connect() as connection:
            expressions = list(map(
                lambda account: update(Account).where(Account.address == account.address).values(
                    balance=account.balance,
                    nonce=account.nonce), accounts))
            for expression in expressions:
                connection.execute(expression)
            connection.commit()

    @staticmethod
    def __map_row_to_object(row: Row) -> Account:
        return Account(address=row[0], nonce=int(row[1]), code_hash=row[2], storage_hash=row[3], balance=int(row[4]))

    def get(self, address: str) -> Optional[Account]:
        with self.engine.connect() as connection:
            expression = select(Account).where(Account.address == address)
            account_row = connection.execute(expression).first()
            if not account_row:
                return None
            return self.__map_row_to_object(account_row)

    def list(self) -> List[Account]:
        with self.engine.connect() as connection:
            expression = select(Account)
            account_rows = connection.execute(expression).fetchall()
            return list(map(self.__map_row_to_object, account_rows))
