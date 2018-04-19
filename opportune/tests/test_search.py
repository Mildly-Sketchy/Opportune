def test_render_search_view(dummy_request):
    """Test search view"""
    from ..views.search import search_view
    response = search_view(dummy_request)
    assert type(response) == dict


def test_search_view_no_keywords(dummy_request):
    """Test search view response when the user does not give any keywords"""
    from ..views.search import search_view
    response = search_view(dummy_request)
    len(response) == 0
    assert type(response) == dict


def test_handle_keywords_view_bad_request(dummy_request):
    '''test handle keywords bad request'''
    from ..views.search import handle_keywords
    from pyramid.httpexceptions import HTTPBadRequest

    dummy_request.method = 'POST'
    response = handle_keywords(dummy_request)
    assert response.status_code == 400
    assert isinstance(response, HTTPBadRequest)


def test_handle_keywords_gets_keyword(dummy_request):
    '''test that it gets the key word'''
    from ..views.search import handle_keywords
    from pyramid.httpexceptions import HTTPFound

    dummy_request.POST = {'keyword': 'web developer'}
    dummy_request.method = 'POST'
    response = handle_keywords(dummy_request)
    assert isinstance(response, HTTPFound)


def test_delete_keyword_view_bad_request(dummy_request):
    '''test delete keywords bad request'''
    from ..views.search import delete_keyword
    from pyramid.httpexceptions import HTTPBadRequest

    dummy_request.method = 'POST'
    response = delete_keyword(dummy_request)
    assert response.status_code == 400
    assert isinstance(response, HTTPBadRequest)
