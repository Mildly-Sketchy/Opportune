def test_constructed_account_added_to_database(db_session):
    """Test adding a complete stock entry."""
    from ..models import Account

    assert len(db_session.query(Account).all()) == 0
    account = Account(
        username='TEST',
        password='1234',
        email='some@email.com',
    )
    db_session.add(account)
    assert len(db_session.query(Account).all()) == 1


def test_account_with_no_email_throws_error(db_session):
    """Test adding stock with required field empty."""
    from ..models import Account
    import pytest
    from sqlalchemy.exc import IntegrityError

    assert len(db_session.query(Account).all()) == 0
    account = Account(
        username='Test2',
        password='1234',
        email=None
    )
    with pytest.raises(IntegrityError):
        db_session.add(account)
        assert db_session.query(Account).one_or_none() is None
