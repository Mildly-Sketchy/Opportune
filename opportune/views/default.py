from pyramid.view import view_config
from pyramid.security import NO_PERMISSION_REQUIRED
from pyramid.response import Response
from ..models import Keyword
from ..models import Association
from . import DB_ERR_MSG


@view_config(route_name='home', renderer='../templates/index.jinja2',
             permission=NO_PERMISSION_REQUIRED)
def home_view(request):
    """Return homepage."""
    return {}


@view_config(route_name='about', renderer='../templates/about.jinja2',
             permission=NO_PERMISSION_REQUIRED)
def about_view(request):
    """Return about page."""
    return {}
