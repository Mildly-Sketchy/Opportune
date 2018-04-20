from pyramid import testing
# from pyramid.response import Response


def test_default_behavior_of_base_view(dummy_request):
    """Test default homepage behavior."""
    from ..views.default import home_view
    response = home_view(dummy_request)
    assert type(response) == dict


def test_default_behavior_of_about_view(dummy_request):
    """Test default about behavior."""
    from ..views.default import about_view
    response = about_view(dummy_request)
    assert len(response) == 0
    assert type(response) == dict


# def test_default_behavior_of_search(dummy_request):
#     """Test default for search behavior"""
#     from ..views.default import search_view
#     response = search_view(dummy_request)
#     assert user_keywords('Seattle') == Seattle
