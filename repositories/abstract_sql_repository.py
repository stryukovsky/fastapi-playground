import abc

from sqlalchemy import Row, Engine


class AbstractSQLRepository(abc.ABC):
    engine: Engine

    def __init__(self, engine: Engine):
        self.engine = engine

    @staticmethod
    @abc.abstractmethod
    def _map_row_to_object(row: Row):
        pass
