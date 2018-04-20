from pyramid.view import view_config
from pyramid.httpexceptions import HTTPUnauthorized
from ..models import Association, Account
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.layouts import gridplot
from bokeh.embed import components
from bokeh.palettes import Spectral6, Spectral5
from bokeh.transform import factor_cmap
import pandas as pd
import numpy as np


@view_config(route_name='stat', renderer='../templates/stat.jinja2',
             request_method='GET')
def stat_view(request):
    try:
        query = request.dbsession.query(Account)
        admin = query.filter(Account.username == request.authenticated_userid).one_or_none()
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

            lang = ['./mass_scraper/pythonresults.csv', './mass_scraper/javascriptresults.csv','./mass_scraper/csharpresults.csv', './mass_scraper/javaresults.csv', './mass_scraper/phpresults.csv', './mass_scraper/cplusresults.csv']
            lang_legend = ['python', 'javascript', 'csharp', 'java', 'php', 'Cplus']
            avg = []
            place_count = 0
            p1 = figure(title="Salaries by Language", background_fill_color="#E8DDCB")
            p1.xaxis[0].formatter.use_scientific = False
            p1.legend.location = "top_center"
            p1.legend.click_policy="hide"
            for lng in lang:
                df = pd.read_csv(lng)
                y = list(df[lang_legend[place_count]])
                avg.append(np.mean(y))
                hist, edges = np.histogram(y)
                p1.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:], fill_color=Spectral6[place_count],
                        fill_alpha=0.3, line_color=Spectral6[place_count], legend=lang_legend[place_count])
                place_count += 1
            p2 = figure(x_range=lang_legend, y_range=(0, max(avg)), plot_height=500, title="Average Salaries by Language")
            source = ColumnDataSource(data=dict(lang_legend=lang_legend, avg=avg))
            p2.vbar(x='lang_legend', top='avg', width=0.9, legend=False, source=source, fill_color=factor_cmap('lang_legend', palette=Spectral6, factors=lang_legend))
            p2.yaxis[0].formatter.use_scientific = False
            
            job = ['./mass_scraper/datascienceresults.csv', './mass_scraper/DBAresults.csv',
                   './mass_scraper/softwaredevresults.csv', './mass_scraper/uxresults.csv', './mass_scraper/webdevresults.csv']
            job_legend = ['datascience', 'dba', 'softwaredev', 'ux', 'webdev']
            avg1 = []
            place_count = 0
            p3 = figure(title="Salaries by Job", background_fill_color="#E8DDCB")
            p3.xaxis[0].formatter.use_scientific = False
            p3.legend.location = "top_center"
            p3.legend.click_policy = "hide"
            for jab in job:
                df = pd.read_csv(jab)
                y = list(df[job_legend[place_count]])
                avg1.append(np.mean(y))
                hist, edges = np.histogram(y)
                p3.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:], fill_color=Spectral5[place_count],
                        fill_alpha=0.3, line_color=Spectral5[place_count], legend=job_legend[place_count])
                place_count += 1
            import pdb; pdb.set_trace()
            p4 = figure(x_range=job_legend, y_range=(0, max(avg1)),
                        plot_height=500, title="Average Salaries by Job")
            source = ColumnDataSource(
                data=dict(job_legend=job_legend, avg1=avg1))
            p4.vbar(x='job_legend', top='avg1', width=0.9, legend=False, source=source,
                    fill_color=factor_cmap('job_legend', palette=Spectral5, factors=job_legend))
            p4.yaxis[0].formatter.use_scientific = False

            all_plots = gridplot([[p1, p3], [p2, p4]])
            script, div = components(all_plots)
            return {'script': script, 'div': div}

    except AttributeError:
        return HTTPUnauthorized()
