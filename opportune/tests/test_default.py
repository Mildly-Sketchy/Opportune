from pyramid import testing
# from pyramid.response import Response


def test_default_behavior_of_base_view(dummy_request):
    """Test default homepage behavior."""
    from ..views.default import home_view
    response = home_view(dummy_request)
    assert type(response) == dict


def test_default_behavior_of_profile_view(dummy_request):
    """Test default profile behavior."""
    from ..views.default import profile_view
    response = profile_view(dummy_request)
    assert type(response) == dict


def test_profile_view_with_no_keywords(dummy_request):
    """Test default profile view with no keywords"""
    from ..views.default import profile_view
    response = profile_view(dummy_request)
    len(response) == 0
    assert type(response) == dict
    assert response == {'message': 'You do not have any keywords saved. Add one!'}


# use with fake authenticated user to test keywords

def test_profile_view_gets_keywords(dummy_request):
    '''Test profile view gets keywords'''
    from ..views.default import profile_view
    # from ..views.default import handle_keywords
    from ..models.accounts import Account
    from ..models.keywords import Keyword
    from ..models.association import Association

    config = testing.setUp()
    
    config.testing_securitypolicy(
        userid='codefellows', permissive=True
    )
    # import pdb; pdb.set_trace()
    new_account = Account(
        username='codefellows',
        password='password',
        email='myemail@gmail.com'
    )
    dummy_request.dbsession.add(new_account)
    
    new_keyword = Keyword()
    new_keyword.keyword = 'developer'
    dummy_request.dbsession.add(new_keyword)

    dummy_request.dbsession.commit()

    new_association = Association()
    new_association.user_id = 'codefellows'
    new_association.keyword_id = 'developer'
    dummy_request.dbsession.add(new_association)

    dummy_request.dbsession.commit()
    
    # dummy_request.authenticated_userid = 'codefellows'
    response = profile_view(dummy_request)

    assert response['keywords'][0].keyword == 'developer'
    
    # assert response == {'keywords': new_keyword}
   
    # dummy_request.GET = {'keywords': 'developer'}
    # dummy_request.method = 'GET'
    # res = profile_view(dummy_request)
    # assert res == {'keywords': 'developer'}



# def test_profile_delete_keyword_works(dummy_request):
#     '''Test delete keyword behaviour'''
#     from ..views.default import delete_keyword_profile
#     from pyramid.httpexceptions import HTTPFound

#     dummy_request.POST = {'keyword': 'web developer'}
#     dummy_request.method = 'POST'
#     response = delete_keyword_profile(dummy_request)
#     assert isinstance(response, HTTPFound)


def test_profile_delete_keyword_bad_request(dummy_request):
    '''Test attempt delete keyword bad request'''
    from ..views.default import delete_keyword_profile
    from pyramid.httpexceptions import HTTPBadRequest

    dummy_request.method = 'POST'
    response = delete_keyword_profile(dummy_request)
    assert response.status_code == 400
    assert isinstance(response, HTTPBadRequest)


def test_default_behavior_of_about_view(dummy_request):
    """Test default about behavior."""
    from ..views.default import about_view
    response = about_view(dummy_request)
    assert len(response) == 0
    assert type(response) == dict
   

def test_render_search_view(dummy_request):
    """Test search view"""
    from ..views.default import search_view
    response = search_view(dummy_request)
    assert type(response) == dict


def test_search_view_no_keywords(dummy_request):
    """Test search view response when the user does not give any keywords"""
    from ..views.default import search_view
    response = search_view(dummy_request)
    len(response) == 0
    assert type(response) == dict


def test_handle_keywords_view_bad_request(dummy_request):
    '''test handle keywords bad request'''
    from ..views.default import handle_keywords
    from pyramid.httpexceptions import HTTPBadRequest

    dummy_request.method = 'POST'
    response = handle_keywords(dummy_request)
    assert response.status_code == 400
    assert isinstance(response, HTTPBadRequest)


# 
def test_handle_keywords_gets_keyword(dummy_request):
    '''test that it gets the key word'''
    from ..views.default import handle_keywords
    from pyramid.httpexceptions import HTTPFound

    dummy_request.POST = {'keyword': 'web developer'}
    dummy_request.method = 'POST'
    response = handle_keywords(dummy_request)
    assert isinstance(response, HTTPFound)


def test_delete_keyword_view_bad_request(dummy_request):
    '''test delete keywords bad request'''
    from ..views.default import delete_keyword
    from pyramid.httpexceptions import HTTPBadRequest

    dummy_request.method = 'POST'
    response = delete_keyword(dummy_request)
    assert response.status_code == 400
    assert isinstance(response, HTTPBadRequest)


def test_default_behavior_of_email_view(dummy_request):
    """Test default email view behavior."""
    from ..views.scraper import email_view
    response = email_view(dummy_request)
    assert len(response) == 0
    assert type(response) == dict


# def test_default_behavior_of_search(dummy_request):
#     """Test default for search behavior"""
#     from ..views.default import search_view
#     response = search_view(dummy_request)
#     assert user_keywords('Seattle') == Seattle