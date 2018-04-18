from pyramid import testing
import os


def substitute_urllib_get_request(self, method, url):
    """Mock response from Indeed website from urllib3."""
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


# def test_default_behavior_of_scraper(dummy_request, monkeypatch):
#     """Test default scraper behavior."""
#     from ..views.scraper import get_jobs
#     from urllib3 import PoolManager
#     # Patching the request to not actually hit the API
#     monkeypatch.setattr(PoolManager, 'request', substitute_urllib_get_request)
#     # import requests
#     # monkeypatch.setattr(requests, 'get', sub_requests_get)

#     dummy_request.method = 'POST'
#     dummy_request.POST = {'city': 'seattle', 'keyword': 'python'}
#     response = get_jobs(dummy_request)
#     # assert len(response) == 0
#     assert type(response) == dict
