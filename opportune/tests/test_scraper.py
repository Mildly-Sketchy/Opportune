from pyramid import testing


def substitute_get_request(method, url):
    # response.data.decode('utf-8')
    class DummyResponse:
        class Data:
            def decode(self, encoding):
                with open('dummy.txt') as f:
                    result = f.read()
                return result
        data = Data()
    return DummyResponse()


def test_default_behavior_of_scraper(dummy_request, monkeypatch):
    """Test default scraper behavior."""
    from ..views.scraper import get_jobs
    import urllib3
    # Patching the request to not actually hit the API
    monkeypatch.setattr(urllib3, 'PoolManager.request', substitute_get_request)

    dummy_request.method = 'POST'
    dummy_request.POST = {'city': 'seattle', 'keyword': 'python'}
    response = get_jobs(dummy_request)
    # assert len(response) == 0
    assert type(response) == dict
