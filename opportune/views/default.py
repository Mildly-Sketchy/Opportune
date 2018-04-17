from pyramid.view import view_config
from pyramid.security import NO_PERMISSION_REQUIRED
from pyramid.httpexceptions import HTTPFound, HTTPBadRequest
from pyramid.response import Response
from sqlalchemy.exc import DBAPIError
from ..models import Account
from ..models import Keyword
from ..models import Association
import smtplib
import os
import csv
from . import DB_ERR_MSG


@view_config(route_name='home', renderer='../templates/index.jinja2',
             permission=NO_PERMISSION_REQUIRED)
def home_view(request):
    """Return homepage."""
    return {}


@view_config(route_name='profile', renderer='../templates/profile.jinja2')
def profile_view(request):
    """Return profile settings page."""
    if request.method == 'GET':
            try:
                query = request.dbsession.query(Keyword)
                user_keywords = query.filter(Association.user_id == request.authenticated_userid, Association.keyword_id == Keyword.keyword)
            except DBAPIError:
                raise DBAPIError(DB_ERR_MSG, content_type='text/plain', status=500)

            keywords = [keyword.keyword for keyword in user_keywords]
            if len(keywords) < 1:
                return{'message': 'You do not have any keywords saved. Add one!'}

            return{'keywords': user_keywords}


@view_config(route_name='profile/delete', renderer='../templates/profile.jinja2')
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


@view_config(route_name='analytics', renderer='../templates/admin.jinja2')
def analytics_view(request):
    """Return employer analytics."""
    return {}


@view_config(route_name='about', renderer='../templates/about.jinja2',
             permission=NO_PERMISSION_REQUIRED)
def about_view(request):
    """Return about page."""
    return {}


@view_config(route_name='search', renderer='../templates/search.jinja2')
def search_view(request):
    """Get user's saved keywords from the database if they exist and render search page."""
    if request.method == 'GET':
            try:
                query = request.dbsession.query(Keyword)
                user_keywords = query.filter(Association.user_id == request.authenticated_userid, Association.keyword_id == Keyword.keyword)
            except DBAPIError:
                raise DBAPIError(DB_ERR_MSG, content_type='text/plain', status=500)

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

        except DBAPIError:
            return Response(DB_ERR_MSG, content_type='text/plain', status=500)

        return HTTPFound(location=request.route_url('search'))


@view_config(route_name='keywords/delete', renderer='../templates/search.jinja2')
def delete_keyword(request):
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

            return HTTPFound(location=request.route_url('search'))

        except DBAPIError:
            return Response(DB_ERR_MSG, content_type='text/plain', status=500)


@view_config(route_name='search/email', renderer='../templates/search.jinja2')
def email_view(request):
    """Send email after scraper has run at user request."""

    if request.method == 'POST':
        with open('./results.csv') as input_file:
            reader = csv.reader(input_file)
            data = list(reader)
        msg = 'Subject: Current Job Listings\n'
        for posting in data:
            msg += '\n'.join(posting) + '\n'*4
        mail_from = os.environ.get('TEST_EMAIL')
        log = os.environ.get('ZZZZZ')
        query = request.dbsession.query(Account).filter(
            Account.username == request.authenticated_userid).first()
        smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
        smtpObj.ehlo()
        smtpObj.starttls()
        smtpObj.login(mail_from, log)
        smtpObj.sendmail(mail_from, query.email, msg)
        smtpObj.quit()
    return {}
