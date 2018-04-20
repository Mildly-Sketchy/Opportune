from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound, HTTPBadRequest
from sqlalchemy.exc import DBAPIError
from . import DB_ERR_MSG
from ..models import Keyword
from ..models import Association
from pyramid.response import Response


@view_config(route_name='search', renderer='../templates/search.jinja2')
def search_view(request):
    """Get user's saved keywords from the database if they exist and render search page."""
    if request.method == 'GET':
            try:
                query = request.dbsession.query(Keyword)
                user_keywords = query.filter(Association.user_id == request.authenticated_userid, Association.keyword_id == Keyword.keyword)
            except KeyError:
                return HTTPFound
            # except DBAPIError:
            #     raise DBAPIError(DB_ERR_MSG, content_type='text/plain', status=500)

            keywords = [keyword.keyword for keyword in user_keywords]
            if len(keywords) < 1:
                return{'message': 'You do not have any keywords saved. Add one!'}

            return{'keywords': user_keywords}


@view_config(route_name='keywords', renderer='../templates/search.jinja2')
def handle_keywords(request):
    """Add and delete keywords in database."""

    if request.method == 'POST':
        try:
            keyword = request.POST['keyword']
        except KeyError:
            return HTTPBadRequest()

        try:
            keyword = int(keyword)
            return {'error': 'Search term cannot be a number.'}
        except ValueError:
            if len(keyword.split()) > 1:
                keyword = keyword.split()
                keyword = '+'.join(keyword)

        instance = Keyword(
            keyword=keyword
        )
        association = Association(
            user_id=request.authenticated_userid,
            keyword_id=instance.keyword
        )

        try:
            keyword_query = request.dbsession.query(Keyword)
            if keyword_query.filter(Keyword.keyword == instance.keyword).first() is None:
                request.dbsession.add(instance)

            if keyword_query.filter(instance.keyword == Association.keyword_id, association.user_id == Association.user_id).first() is None:
                request.dbsession.add(association)
            else:
                return{'message': 'You have already saved that keyword.'}

        except DBAPIError:  # pragma: no cover
            return Response(DB_ERR_MSG, content_type='text/plain', status=500)

        return HTTPFound(location=request.route_url('search'))


@view_config(route_name='keywords/delete', renderer='../templates/search.jinja2')
def delete_keyword(request):
    """Delete a requested keyword from association table for that particular user."""
    if request.method == 'POST':
        try:
            keyword = request.POST['keyword']
            user = request.authenticated_userid
        except KeyError:  # pragma: no cover
            return HTTPBadRequest()

        try:  # pragma: no cover
            query = request.dbsession.query(Association)
            removed = query.filter(Association.keyword_id == keyword, Association.user_id == user).one()

            request.dbsession.delete(removed)

            return HTTPFound(location=request.route_url('search'))

        except DBAPIError:  # pragma: no cover
            return Response(DB_ERR_MSG, content_type='text/plain', status=500)
