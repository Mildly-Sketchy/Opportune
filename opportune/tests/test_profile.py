from pyramid import testing


def test_default_behavior_of_profile_view(dummy_request):
    """Test default profile behavior."""
    from ..views.profile import profile_view
    response = profile_view(dummy_request)
    assert type(response) == dict


def test_profile_view_with_no_keywords(dummy_request):
    """Test default profile view with no keywords"""
    from ..views.profile import profile_view
    response = profile_view(dummy_request)
    len(response) == 0
    assert type(response) == dict
    assert response == {'message': 'You do not have any keywords saved. Add one!'}


def test_profile_view_gets_keywords(dummy_request):
    '''Test profile view returns keywords with fake authenticated user'''
    from ..views.profile import profile_view
    from ..models.accounts import Account
    from ..models.keywords import Keyword
    from ..models.association import Association

    config = testing.setUp()

    config.testing_securitypolicy(
        userid='codefellows', permissive=True
    )
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

    response = profile_view(dummy_request)

    assert response['keywords'][0].keyword == 'developer'


def test_profile_update_email(dummy_request):
    '''Test bad attempt update email'''
    from ..views.profile import update_email
    from pyramid.httpexceptions import HTTPBadRequest

    dummy_request.method = 'POST'
    response = update_email(dummy_request)
    assert response.status_code == 400
    assert isinstance(response, HTTPBadRequest)


def test_profile_delete_keyword_profile_works(dummy_request):
    '''Test delete keyword behaviour'''
    from ..views.profile import delete_keyword_profile
    from ..models.accounts import Account
    from ..models.keywords import Keyword
    from ..models.association import Association

    config = testing.setUp()
    config.include('opportune.routes')

    config.testing_securitypolicy(
        userid='codefellows', permissive=True
    )
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

    dummy_request.method = 'POST'
    dummy_request.POST = {'keyword': 'developer'}

    response = delete_keyword_profile(dummy_request)
    assert response.status_code == 200


def test_profile_delete_keyword_bad_request(dummy_request):
    '''Test attempt delete keyword bad request'''
    from ..views.profile import delete_keyword_profile
    from pyramid.httpexceptions import HTTPBadRequest

    dummy_request.method = 'POST'
    response = delete_keyword_profile(dummy_request)
    assert response.status_code == 400
    assert isinstance(response, HTTPBadRequest)
