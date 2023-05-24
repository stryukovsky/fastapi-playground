from typing import List

from sqlalchemy import create_engine, String, BigInteger, ForeignKeyConstraint, ForeignKey, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)


class Base(DeclarativeBase):
    pass


class Account(Base):
    __tablename__ = "account"

    address: Mapped[str] = mapped_column(String(42), unique=True, primary_key=True)
    nonce: Mapped[int] = mapped_column(BigInteger(), default=0)
    code_hash: Mapped[str] = mapped_column(String(66), default="")
    storage_hash: Mapped[str] = mapped_column(String(66), default="")
    balance: Mapped[int] = mapped_column(BigInteger(), default=0)

    owned_tokens: Mapped[List["Token"]] = relationship(back_populates="owner", cascade="all, delete-orphan")
    token_balances: Mapped[List["TokenBalance"]] = relationship(back_populates="account", cascade="all, delete-orphan")


class Token(Base):
    __tablename__ = "token"

    address: Mapped[str] = mapped_column(String(42), primary_key=True, unique=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    ticker: Mapped[str] = mapped_column(String(255), unique=True)
    total_supply: Mapped[int] = mapped_column(BigInteger(), default=0)

    owner_address: Mapped[str] = mapped_column(ForeignKey("account.address"))
    owner: Mapped["Account"] = relationship(back_populates="owned_tokens")

    account_balances: Mapped[List["TokenBalance"]] = relationship(back_populates="token", cascade="all, delete-orphan")


class TokenBalance(Base):
    __tablename__ = "token_balance"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    amount: Mapped[int] = mapped_column(BigInteger(), default=0)

    token: Mapped["Token"] = relationship(back_populates="account_balances")
    token_address: Mapped[str] = mapped_column(ForeignKey("token.address"))

    account: Mapped["Account"] = relationship(back_populates="token_balances")
    account_address: Mapped[str] = mapped_column(ForeignKey("account.address"))


Base.metadata.create_all(engine)
