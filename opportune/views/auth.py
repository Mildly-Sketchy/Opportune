from pyramid.httpexceptions import HTTPFound, HTTPBadRequest, HTTPUnauthorized
from pyramid.security import NO_PERMISSION_REQUIRED, remember, forget
from pyramid.response import Response
from sqlalchemy.exc import DBAPIError
from pyramid.view import view_config
from ..models import Account
from . import DB_ERR_MSG


@view_config(
    route_name='auth',
    renderer='../templates/auth.jinja2',
    permission=NO_PERMISSION_REQUIRED)
def auth_view(request):
    if request.authenticated_userid:
        return HTTPFound(location=request.route_url('profile'))

    if request.method == 'POST':
        try:
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']

        except KeyError:
            return HTTPBadRequest()

        try:
            instance = Account(
                username=username,
                email=email,
                password=password,
            )

            query = request.dbsession.query(Account)
            if query.filter(Account.username == username).first() is None:
                headers = remember(request, userid=instance.username)
                request.dbsession.add(instance)

            else:
                return {'message': 'That username is already in use.'}

            return HTTPFound(location=request.route_url('search'), headers=headers)

        except DBAPIError:
            return Response(DB_ERR_MSG, content_type='text/plain', status=500)

    if request.method == 'GET':
        try:
            username = request.GET['username']
            password = request.GET['password']

        except KeyError:
            return {}

        is_authenticated = Account.check_credentials(request, username, password)
        if is_authenticated[0]:
            headers = remember(request, userid=username)
            return HTTPFound(location=request.route_url('search'), headers=headers)
        else:
            return HTTPUnauthorized()

    return HTTPFound(location=request.route_url('home'))


@view_config(route_name='logout')
def logout(request):
    """Log out of current account."""
    headers = forget(request)
    return HTTPFound(location=request.route_url('home'), headers=headers)
