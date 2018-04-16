from sqlalchemy import (
    Index,
    Column,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from .meta import Base


class Keyword(Base):
    __tablename__ = 'keywords'
    id = Column(Integer, primary_key=True)
    keyword = Column(String, nullable=False, unique=True)

    accounts = relationship(
        'Account',
        secondary='user_keywords')


Index('entry_index', Keyword.id, unique=True, mysql_length=255)
 