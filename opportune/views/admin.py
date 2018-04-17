from pyramid.httpexceptions import HTTPFound, HTTPBadRequest, HTTPUnauthorized, HTTPNotFound
from pyramid.security import NO_PERMISSION_REQUIRED, remember, forget
from pyramid.response import Response
from sqlalchemy.exc import DBAPIError
from pyramid.view import view_config
from ..models import Account, Association
from . import DB_ERR_MSG
import csv

def read_file():
    """read the file and reutnr the data in a suitable format"""

@view_config(route_name='analytics', 
    renderer='../templates/admin.jinja2',
    request_method = 'GET')
def analytics_view(request):
    """Return employer analytics."""
    test = []
    with open('./results.csv') as infile:
        data = csv.DictReader(infile)
        for row in data:
            test.append(row)
            
    return {'data':test}