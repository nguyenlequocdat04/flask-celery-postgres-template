from sqlalchemy import inspect, Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.extensions import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    created_by = Column(Integer, ForeignKey("sample.user.id"))
    created_by_user = relationship("User", foreign_keys=[created_by], lazy='subquery')

    __table_args__ = (
        {"schema": "sample"},
    )

    def to_json(self):
        json_item = {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
        json_item['created_by'] = self.created_by_user.email if self.created_by_user else ''
        return json_item
