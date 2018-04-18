from pyramid.view import view_config
from ..models import Keyword, Association
from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.embed import components


@view_config(route_name='stat', renderer='../templates/stat.jinja2',
             request_method='GET')
def stat_view(request):
    relationships = request.dbsession.query(Association)
    count = {}
    keys = request.dbsession.query(Keyword)
    for each in relationships:
        word = keys.get(each.keyword_id).keyword
        if word not in count:
            count[word] = 1
        else:
            count[word] += 1
    users = list(count.values())
    keywords = list(count.keys())
    source = ColumnDataSource(data=dict(keywords=keywords, users=users))
    p = figure(x_range=keywords, y_range=(0, 5), plot_height=250,
               title="Search Counts")
    p.vbar(x='keywords', top='users', width=0.9, legend="keywords",
           source=source)
    p.xgrid.grid_line_color = None
    p.legend.orientation = "horizontal"
    p.legend.location = "top_center"
    script, div = components(p)
    return {'script': script, 'div': div}
