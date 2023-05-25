import abc
from typing import Optional, List

from sqlalchemy import select, Row, update
from sqlalchemy.orm import Session

from database import Account, Token, TokenBalance
from .abstract_sql_repository import AbstractSQLRepository


class TokensRepository(abc.ABC):

    @abc.abstractmethod
    def deploy_token(self, deployer: Account, address: str, name: str, ticker: str, initial_supply: int):
        pass

    @abc.abstractmethod
    def get_by_address(self, address: str) -> Optional[Token]:
        pass

    @abc.abstractmethod
    def get_by_name(self, name: str) -> Optional[Token]:
        pass

    @abc.abstractmethod
    def get_by_ticker(self, ticker: str) -> Optional[Token]:
        pass

    @abc.abstractmethod
    def list(self) -> List[Token]:
        pass


class SQLTokensRepository(TokensRepository, AbstractSQLRepository):

    def list(self) -> List[Token]:
        with self.engine.connect() as connection:
            expression = select(Token)
            rows = connection.execute(expression).fetchall()
            return list(map(self._map_row_to_object, rows))

    def deploy_token(self, deployer: Account, address: str, name: str, ticker: str, initial_supply: int):
        with Session(self.engine) as session:
            session.add(
                Token(address=address, name=name, ticker=ticker, total_supply=initial_supply,
                      owner_address=deployer.address))
            session.add(TokenBalance(amount=initial_supply, token_address=address, account_address=deployer.address))
            nonce_update_statement = update(Account).where(Account.address == deployer.address).values({
                "nonce": deployer.nonce
            })
            session.execute(nonce_update_statement)
            session.commit()

    @staticmethod
    def _map_row_to_object(row: Row) -> Token:
        return Token(address=row[0], name=row[1], ticker=row[2], total_supply=row[3], owner_address=row[4])

    def get_by_address(self, address: str) -> Optional[Token]:
        with self.engine.connect() as connection:
            expression = select(Token).where(Token.address == address)
            if not (row := connection.execute(expression).first()):
                return None
            else:
                return self._map_row_to_object(row)

    def get_by_name(self, name: str) -> Optional[Token]:
        with self.engine.connect() as connection:
            expression = select(Token).where(Token.name == name)
            if not (row := connection.execute(expression).first()):
                return None
            else:
                return self._map_row_to_object(row)

    def get_by_ticker(self, ticker: str) -> Optional[Token]:
        with self.engine.connect() as connection:
            expression = select(Token).where(Token.ticker == ticker)
            if not (row := connection.execute(expression).first()):
                return None
            else:
                return self._map_row_to_object(row)
