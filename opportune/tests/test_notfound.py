from pyramid import testing
# from pyramid.response import Response


def test_default_behavior_of_notfound_view(dummy_request):
    """Test default notfound behavior."""
    from ..views.notfound import notfound_view
    response = notfound_view(dummy_request)
    assert len(response) == 0
    assert type(response) == dict
