def test_get_stat_view(dummy_request, db_session, test_user):
    """Test default stat behavior."""
    from ..views.stat import stat_view
    from pyramid.httpexceptions import HTTPUnauthorized
    response = stat_view(dummy_request)

    assert isinstance(response, HTTPUnauthorized)
