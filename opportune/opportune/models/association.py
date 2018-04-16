from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
)

from .meta import Base


class Association(Base):
    """Association table for users and keywords."""
    __tablename__ = 'user_keywords'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    keyword_id = Column(Integer, ForeignKey('keywords.id'), nullable=False)
