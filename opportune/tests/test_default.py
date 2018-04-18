from pyramid import testing
# from pyramid.response import Response


def test_default_behavior_of_base_view(dummy_request):
    """Test default homepage behavior."""
    from ..views.default import home_view
    response = home_view(dummy_request)
    assert len(response) == 0
    assert type(response) == dict


# fix:

# def test_default_behavior_of_profile_view(dummy_request):
#     """Test default profile behavior."""
#     from ..views.default import profile_view
#     response = profile_view(dummy_request)
#     assert isinstance(response, dict)


# def test_delete_keyword_bad_request(dummy_request):
#     '''test bad request'''
#     from ..views.default import delete_keyword
#     from pyramid.httpexceptions import HTTPBadRequest

#     dummy_request.POST = ['keyword']
#     dummy_request.method = 'POST'
#     response = delete_keyword(dummy_request)
#     assert response.status_code == 400
#     assert isinstance(response, HTTPBadRequest)


def test_search_view():
    pass


def test_handle_keyword():
    pass


def test_delete_keyword():
    pass


def test_default_behavior_of_analytics_view(dummy_request):
    """Test default analytics behavior."""
    from ..views.default import analytics_view
    response = analytics_view(dummy_request)
    assert len(response) == 0
    assert type(response) == dict


def test_default_behavior_of_about_view(dummy_request):
    """Test default about behavior."""
    from ..views.default import about_view
    response = about_view(dummy_request)
    assert len(response) == 0
    assert type(response) == dict


def test_default_behavior_of_email_view(dummy_request):
    """Test default email view behavior."""
    from ..views.default import email_view
    response = email_view(dummy_request)
    assert len(response) == 0
    assert type(response) == dict
