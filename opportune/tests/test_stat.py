def test_get_stat_view(dummy_request, db_session, test_user):
    """Test default stat behavior."""
    from ..views.stat import stat_view
    from pyramid.httpexceptions import HTTPUnauthorized
    response = stat_view(dummy_request)

    assert isinstance(response, HTTPUnauthorized)


# def test_admin_user_on_stat_page(dummy_request, db_session, test_user):
#     """Test admin user on stat page"""
#     from ..views.stat import stat_view
#     from ..views.auth import auth_view
#     db_session.add(test_user)
#     # dummy_request.GET = {'username': 'testtest', 'password': 'testpass'}
#     # dummy_request.method = 'GET'
#     # response = stat_view(auth_view(dummy_request))
#     assert type(response) == dict
    