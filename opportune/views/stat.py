from pyramid.view import view_config
from pyramid.httpexceptions import HTTPUnauthorized, HTTPFound
from ..models import Association, Account
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.embed import components
from sqlalchemy.exc import DBAPIError
from . import DB_ERR_MSG


@view_config(route_name='stat', renderer='../templates/stat.jinja2',
             request_method='GET')
def stat_view(request):
    try:
        query = request.dbsession.query(Account)
<<<<<<< HEAD
        admin = query.filter(Account.username == request.authenticated_userid).one()

=======
        admin = query.filter(Account.username == request.authenticated_userid).one_or_none()
>>>>>>> 3613b24fbfbc87e9fd19b8c80f61bf7e1fc70c2c
        if admin.admin is True:
            relationships = request.dbsession.query(Association)
            count = {}
            for each in relationships:
                word = each.keyword_id
                if word not in count:
                    count[word] = 1
                else:
                    count[word] += 1
            top = 1
            for value in count.values():
                if top <= value:
                    top = value * 1.5
            users = list(count.values())
            keywords = list(count.keys())
            source = ColumnDataSource(data=dict(keywords=keywords, users=users))
            p = figure(x_range=keywords, y_range=(0, top), plot_height=500,
                       title="Current Stored Searches")
            p.vbar(x='keywords', top='users', width=0.9, legend=False,
                   source=source)
            p.xgrid.grid_line_color = None
            p.legend.orientation = "horizontal"
            p.legend.location = "top_center"
            script, div = components(p)
            return {'script': script, 'div': div}

    except AttributeError:
        return HTTPUnauthorized()
