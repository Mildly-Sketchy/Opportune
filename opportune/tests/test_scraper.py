from pyramid import testing
import os


def substitute_urllib_get_request(self, method, url):
    # response.data.decode('utf-8')
    class DummyResponse:
        class Data:
            def decode(self, encoding):
                # path to the currently running file
                curr_file = os.path.dirname(os.path.abspath(__file__))
                dummy_file = os.path.join(curr_file, 'dummy.txt')
                with open(dummy_file) as f:
                    result = f.read()
                return result
        data = Data()
    return DummyResponse()


def sub_requests_get(url):
    class DummyResponse:
        def __init__(self):
            curr_file = os.path.dirname(os.path.abspath(__file__))
            dummy_file = os.path.join(curr_file, 'dummy.txt')
            with open(dummy_file) as f:
                result = f.read()
            self.text = result
    return DummyResponse()


def test_default_behavior_of_scraper(dummy_request, monkeypatch):
    """Test default scraper behavior."""
    from ..views.scraper import get_jobs
    from urllib3 import PoolManager
    # Patching the request to not actually hit the API
    monkeypatch.setattr(PoolManager, 'request', substitute_urllib_get_request)
    # import requests
    # monkeypatch.setattr(requests, 'get', sub_requests_get)

    dummy_request.method = 'POST'
    dummy_request.POST = {'city': 'seattle', 'keyword': 'python'}
    response = get_jobs(dummy_request)
    # assert len(response) == 0
    assert type(response) == dict


# def test_scraper(dummy_request, monkeypatch):
#     ''''''
#     from ..views.scraper import get_jobs
#     from urllib3 import PoolManager

#     monkeypatch.setattr(PoolManager, 'request', substitute_urllib_get_request)
#     dummy_request.method = 'POST'
#     dummy_request.POST = {'city': 'seattle', 'keyword': 'python'}
#     # response = get_jobs(dummy_request)
    


def test_scraper_bad_request(dummy_request):
    from ..views.scraper import get_jobs
    from pyramid.httpexceptions import HTTPBadRequest

    dummy_request.method = 'POST'
    response = get_jobs(dummy_request)
    assert response.status_code == 400
    assert isinstance(response, HTTPBadRequest)


def test_default_behavior_of_email_view(dummy_request):
    """Test default email view behavior."""
    from ..views.scraper import email_view
    response = email_view(dummy_request)
    assert len(response) == 0
    assert type(response) == dict

