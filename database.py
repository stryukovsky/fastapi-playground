from sqlalchemy import create_engine, String, BigInteger
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

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


Base.metadata.create_all(engine)
