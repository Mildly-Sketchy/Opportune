from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    String
)

from .meta import Base


class Association(Base):
    """Association table for users and keywords."""
    __tablename__ = 'user_keywords'
    id = Column(Integer, primary_key=True)
    user_id = Column(String, ForeignKey('accounts.username'), nullable=False)
    keyword_id = Column(String, ForeignKey('keywords.keyword'), nullable=False)
