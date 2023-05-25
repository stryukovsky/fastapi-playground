import abc
from typing import List, Optional

from sqlalchemy import Row, select, update
from sqlalchemy.orm import Session

from database import TokenBalance, Account

from .abstract_sql_repository import AbstractSQLRepository


class TokenBalancesRepository(abc.ABC):

    @abc.abstractmethod
    def get_by_holder_and_token(self, holder: str, token: str):
        pass

    @abc.abstractmethod
    def create(self, token: str, account: str):
        pass

    @abc.abstractmethod
    def apply_transfer_transaction(self, sender: Account, from_balance: TokenBalance, to_balance: TokenBalance):
        pass

    @abc.abstractmethod
    def get_balances_by_token(self, token: str) -> List[TokenBalance]:
        pass

    @abc.abstractmethod
    def get_balances_by_holder(self, holder: str) -> List[TokenBalance]:
        pass


class SQLTokenBalancesRepository(TokenBalancesRepository, AbstractSQLRepository):
    def create(self, token: str, account: str):
        with Session(self.engine) as session:
            session.add(TokenBalance(token_address=token, account_address=account))
            session.commit()

    @staticmethod
    def _map_row_to_object(row: Row) -> TokenBalance:
        return TokenBalance(id=row[0], amount=row[1], token_address=row[2], account_address=row[3])

    def get_by_holder_and_token(self, holder: str, token: str) -> Optional[TokenBalance]:
        with self.engine.connect() as connection:
            expression = select(TokenBalance)\
                .where(TokenBalance.account_address == holder)\
                .where(TokenBalance.token_address == token)
            if not (row := connection.execute(expression).first()):
                return None
            return self._map_row_to_object(row)

    def apply_transfer_transaction(self, sender: Account, from_balance: TokenBalance, to_balance: TokenBalance):
        with self.engine.connect() as connection:
            apply_from_balance = update(TokenBalance).where(TokenBalance.id == from_balance.id).values({
                "amount": from_balance.amount
            })
            apply_to_balance = update(TokenBalance).where(TokenBalance.id == to_balance.id).values({
                "amount": to_balance.amount
            })
            apply_nonce = update(Account).where(Account.address == from_balance.account_address).values({
                "nonce": sender.nonce
            })
            connection.execute(apply_from_balance)
            connection.execute(apply_to_balance)
            connection.execute(apply_nonce)
            connection.commit()

    def get_balances_by_token(self, token: str) -> List[TokenBalance]:
        with self.engine.connect() as connection:
            expression = select(TokenBalance).where(TokenBalance.token_address == token)
            rows = connection.execute(expression).fetchall()
            return list(map(self._map_row_to_object, rows))

    def get_balances_by_holder(self, holder: str) -> List[TokenBalance]:
        with self.engine.connect() as connection:
            expression = select(TokenBalance).where(TokenBalance.account_address == holder)
            rows = connection.execute(expression).fetchall()
            return list(map(self._map_row_to_object, rows))
