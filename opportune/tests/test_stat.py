def test_get_stat_view_error(dummy_request, db_session, test_user):
    """Test default stat behavior."""
    from ..views.stat import stat_view
    from pyramid.httpexceptions import HTTPUnauthorized
    response = stat_view(dummy_request)

    assert isinstance(response, HTTPUnauthorized)


def test_get_stat_view(dummy_request, db_session, test_user):
    """Test default stat behavior."""
    from ..views.stat import stat_view
    from ..models.accounts import Account
    from pyramid import testing

    config = testing.setUp()

    config.testing_securitypolicy(
        userid='codefellows', permissive=True
    )
    new_account = Account(
        username='codefellows',
        password='password',
        email='myemail@gmail.com',
        admin=True
    )
    dummy_request.dbsession.add(new_account)

    dummy_request.dbsession.commit()

    response = stat_view(dummy_request)

    assert type(response) == dict
