from .meta import Base
from sqlalchemy.exc import DBAPIError
from cryptacular import bcrypt
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
)

manager = bcrypt.BCRYPTPasswordManager()


class Account(Base):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False)
    admin = Column(Boolean, nullable=False, default=False)

    keywords = relationship(
        'Keyword',
        secondary='user_keywords')

    def __init__(self, username, email, password, admin=False):
        """Initialize a new user with encoded password."""
        self.username = username
        self.email = email
        self.password = manager.encode(password, 10)
        self.admin = admin

    @classmethod
    def check_credentials(cls, request=None, username=None, password=None):
        """Authenticate a user."""
        if request.dbsession is None:
            raise DBAPIError

        is_authenticated = False

        query = request.dbsession.query(cls).filter(cls.username == username).one_or_none()

        if query is not None:
            if manager.check(query.password, password):
                is_authenticated = True

        return (is_authenticated, username)
