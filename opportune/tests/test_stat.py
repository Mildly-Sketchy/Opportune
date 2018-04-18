def test_get_auth_view(dummy_request):
    """Test default stat behavior."""
    from ..views.stat import stat_view
    response = stat_view(dummy_request)
    assert isinstance(response, dict)


