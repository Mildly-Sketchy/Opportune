def test_constructed_keyword_added_to_database(db_session):
    """Test adding a keyword."""
    from ..models import Keyword

    assert len(db_session.query(Keyword).all()) == 0
    keyword = Keyword(
        keyword='python'
    )
    db_session.add(keyword)
    assert len(db_session.query(Keyword).all()) == 1

