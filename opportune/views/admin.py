from pyramid.httpexceptions import HTTPFound, HTTPBadRequest, HTTPUnauthorized
from pyramid.security import NO_PERMISSION_REQUIRED, remember, forget
from pyramid.response import Response
from sqlalchemy.exc import DBAPIError
from pyramid.view import view_config
from ..models import Account
from . import DB_ERR_MSG
import csv

data = [1, 2, 3, 4, 5, 6, 7, 8, 9]

def read_file():
    """read the file and reutnr the data in a suitable format"""

@view_config(route_name='analytics', 
    renderer='../templates/admin.jinja2')

def analytics_view(request):
    """Return employer analytics."""
    if request.method == 'POST':

        if 'symbol' not in request.POST:
            return HTTPNotFound()
        symbol = request.POST['symbol']
        response = requests.get('{}/stock/{}/company'.format(API_URL, symbol))
        if response.status_code == 200:
            try:
                query = request.dbsession.query(Entry)
                stock = query.filter(Entry.symbol == symbol).one_or_none()
            except DBAPIError:
                return DBAPIError(
                    DB_ERR_MSG, content_type='text/plain', status=500)
            if stock is None:
                request.dbsession.add(Entry(**response.json()))
            else:
                for key, value in response.json().items():
                    setattr(stock, key, value)
            return HTTPFound(location=request.route_url('portfolio'))
        return HTTPNotFound()
    try:
        # import pdb; pdb.set_trace()
        symbol = request.GET['symbol']
    except KeyError:
        return {}
    response = requests.get('{}/stock/{}/company'.format(API_URL, symbol))
    if response.status_code == 404:
        return {
            'message': f'''{
                symbol.upper()
            } is not available: ({
                request.text
            })'''
            }
    if response.status_code == 200:
        return {
            'company': response.json()
        }

#     with open('mockup_csv/testing.csv') as lofty_data:
#         reader = csv.reader(lofty_data)
#         stats = list(reader)
#         # import pdb; pdb.set_trace()
#     return {}

# def CSVRenderer(request):
#     """Render CSV File"""
    