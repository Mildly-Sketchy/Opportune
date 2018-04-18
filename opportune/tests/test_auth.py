def test_get_auth_view(dummy_request):
    """Test default auth page behavior."""
    from ..views.auth import auth_view
    response = auth_view(dummy_request)
    assert isinstance(response, dict)


def test_auth_signup_view(dummy_request):
    """Test successful signup."""
    from ..views.auth import auth_view
    from pyramid.httpexceptions import HTTPFound

    dummy_request.POST = {'username': 'kat', 'password': '1234', 'email': 'kat@kat.com'}
    dummy_request.method = 'POST'
    response = auth_view(dummy_request)
    assert response.status_code == 302
    assert isinstance(response, HTTPFound)


def test_auth_signin_view(dummy_request):
    """Test successful sign in."""
    from ..views.auth import auth_view
    from pyramid.httpexceptions import HTTPFound

    dummy_request.POST = {'username': 'kat', 'password': '1234', 'email': 'kat@kat.com'}
    dummy_request.method = 'POST'
    auth_view(dummy_request)

    dummy_request.GET = {'username': 'kat', 'password': '1234'}
    dummy_request.method = 'GET'
    response = auth_view(dummy_request)
    assert response.status_code == 302
    assert isinstance(response, HTTPFound)


def test_logout_default(dummy_request):
    """Test logout method returns HTTPFound"""
    from ..views.auth import logout
    from pyramid.httpexceptions import HTTPFound

    response = logout(dummy_request)
    assert isinstance(response, HTTPFound)


def test_bad_request_auth_signup_view(dummy_request):
    """Test bad signup."""
    from ..views.auth import auth_view
    from pyramid.httpexceptions import HTTPBadRequest

    dummy_request.POST = {'password': 'test', 'email': 'test@test.com'}
    dummy_request.method = 'POST'
    response = auth_view(dummy_request)
    assert response.status_code == 400
    assert isinstance(response, HTTPBadRequest)


def test_bad_request_method_auth_signup_view(dummy_request):
    """Test bad method for signup."""
    from ..views.auth import auth_view
    from pyramid.httpexceptions import HTTPFound

    dummy_request.POST = {'password': 'test', 'email': 'test@test.com'}
    dummy_request.method = 'PUT'
    response = auth_view(dummy_request)
    assert response.status_code == 302
    assert isinstance(response, HTTPFound)