from pyramid import testing
# from pyramid.response import Response


def test_default_behavior_of_base_view(dummy_request):
    """Test default homepage behavior."""
    from ..views.default import home_view
    response = home_view(dummy_request)
    assert len(response) == 0
    assert type(response) == dict


def test_default_behavior_of_profile_view(dummy_request):
    """Test default profile behavior."""
    from ..views.default import profile_view
    response = profile_view(dummy_request)
    assert len(response) == 0
    assert type(response) == dict


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
