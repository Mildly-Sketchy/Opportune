from pyramid import testing
import pytest
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
    monkeypatch.setattr(PoolManager, 'request', substitute_urllib_get_request)

    dummy_request.method = 'POST'
    dummy_request.POST = {'city': 'seattle', 'keyword': 'python'}
    response = get_jobs(dummy_request)
    assert type(response) == dict


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


def test_file_download_status_code(dummy_request):
    """Test file download function returns 200 status code."""
    from ..views.scraper import download_results
    response = download_results(dummy_request)
    assert response.status_code == 200


def test_file_download_type(dummy_request):
    """Test file download returns a csv."""
    from ..views.scraper import download_results
    response = download_results(dummy_request)
    assert response.content_type == 'text/csv'


# def test_scraper_output(dummy_request, monkeypatch):
#     from ..views.scraper import get_jobs
#     from urllib3 import PoolManager
#     monkeypatch.setattr(PoolManager, 'request', substitute_urllib_get_request)

#     dummy_request.method = 'POST'
#     dummy_request.POST = {'city': 'seattle', 'keyword': 'python'}
#     response = get_jobs(dummy_request)
