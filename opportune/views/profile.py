from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound, HTTPBadRequest
from pyramid.security import forget
from ..models import Keyword
from ..models import Association
from ..models import Account
from sqlalchemy.exc import DBAPIError
from pyramid.response import Response
from . import DB_ERR_MSG


@view_config(route_name='profile', renderer='../templates/profile.jinja2')
def profile_view(request):
    """Return profile settings page."""
    if request.method == 'GET':
        query = request.dbsession.query(Keyword)
        user_keywords = query.filter(Association.user_id == request.authenticated_userid, Association.keyword_id == Keyword.keyword)

        keywords = [keyword.keyword for keyword in user_keywords]
        if len(keywords) < 1:
            return{'message': 'You do not have any keywords saved. Add one!'}

        return{'keywords': user_keywords}


@view_config(route_name='profile/update', renderer='../templates/profile.jinja2')
def update_email(request):
    """Allow user to update email address."""
    try:
        updated_email = request.POST['email']
    except KeyError:
        return HTTPBadRequest()
    try:
        query = request.dbsession.query(Account)
        user = query.filter(Account.username == request.authenticated_userid).one()
        user.email = updated_email
    except DBAPIError:
        return Response(DB_ERR_MSG, content_type='text/plain', status=500)

    return HTTPFound(location=request.route_url('profile'))


@view_config(route_name='profile/delete', renderer='../templates/profile.jinja2')
def delete_account(request):
    """Allow user to update email address."""
    try:
        query = request.dbsession.query(Account)
        removed = query.filter(Account.username == request.authenticated_userid).one()
        request.dbsession.delete(removed)

        return HTTPFound(location=request.route_url('logout'))
    except KeyError:
        return HTTPBadRequest()

    return HTTPFound(location=request.route_url('home'))


@view_config(route_name='profile/keywords/delete', renderer='../templates/profile.jinja2')
def delete_keyword_profile(request):
    """Delete a requested keyword from association table for that particular user."""
    if request.method == 'POST':
        try:
            keyword = request.POST['keyword']
            user = request.authenticated_userid
        except KeyError:
            return HTTPBadRequest()

        try:

            query = request.dbsession.query(Association)
            removed = query.filter(Association.keyword_id == keyword, Association.user_id == user).one()

            request.dbsession.delete(removed)

            return HTTPFound(location=request.route_url('profile'))

        except DBAPIError:
            return Response(DB_ERR_MSG, content_type='text/plain', status=500)
