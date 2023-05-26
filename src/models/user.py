from sqlalchemy import inspect, Column, Integer, String

from src.extensions import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    name = Column(String)

    __table_args__ = (
        {"schema": "sample"},
    )

    def to_json(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}