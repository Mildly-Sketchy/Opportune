import requests
from bs4 import BeautifulSoup
from pyramid.view import view_config
from ..models import Account
from ..models import Keyword
from ..models import Association
from sqlalchemy.exc import DBAPIError
from pyramid.response import FileResponse
from pyramid.httpexceptions import HTTPBadRequest, HTTPFound
from . import DB_ERR_MSG
import urllib3
import pandas as pd
import csv
import smtplib
import os
import csv


@view_config(route_name='search/results', renderer='../templates/results.jinja2')
def get_jobs(request):  # pragma: no cover
    if request.method == 'POST':

        query = request.dbsession.query(Keyword)
        keyword_query = query.filter(Association.user_id == request.authenticated_userid, Association.keyword_id == Keyword.keyword).all()
        keywords = [keyword.keyword for keyword in keyword_query]

        try:
            city = request.POST['city']
        except KeyError:
            return HTTPBadRequest()

        url_template = 'https://www.indeed.com/jobs?q={}&l={}'
        max_results = 30

        df = pd.DataFrame(columns=['location', 'company', 'job_title', 'salary', 'job_link'])
        requests.packages.urllib3.disable_warnings()
        for keyword in keywords:
            for start in range(0, max_results):
                url = url_template.format(keyword, city)
                http = urllib3.PoolManager()
                response = http.request('GET', url)
                soups = BeautifulSoup(response.data.decode('utf-8'), 'html.parser')
                for b in soups.find_all('div', attrs={'class': ' row result'}):
                    location = b.find('span', attrs={'class': 'location'}).text
                    job_title = b.find('a', attrs={'data-tn-element': 'jobTitle'}).text
                    base_url = 'http://www.indeed.com'
                    href = b.find('a').get('href')
                    job_link = f'{base_url}{href}'
                    try:
                        company = b.find('span', attrs={'class': 'company'}).text
                    except AttributeError:
                        company = 'Not Listed'
                    try:
                        salary = b.find('span', attrs={'class': 'no-wrap'}).text
                    except AttributeError:
                        salary = 'Not Listed'
                    try:
                        summary = b.find('span', {'class':'summary'}).text
                    except AttributeError:
                        summary = 'Not Listed'
                    df = df.append({'location': location, 'company': company,
                                    'job_title': job_title,
                                    'salary': salary, 'summary': summary,
                                    'job_link': job_link}, ignore_index=True)

        df.company.replace(regex=True,inplace=True,to_replace='\n',value='')
        df.salary.replace(regex=True,inplace=True,to_replace='\n',value='')
        df.summary.replace(regex=True, inplace=True, to_replace=u"\u2018", value="'")
        df.summary.replace(regex=True, inplace=True, to_replace=u"\u2019", value="'")
        df.summary.replace(regex=True, inplace=True, to_replace=u"\u2013", value="'")
        cleaned = df.drop_duplicates(['job_link'])
        output = cleaned.head(30)
        output.to_csv('results.csv', index=False)
        results = []
        with open('./results.csv') as infile:
            data = csv.DictReader(infile)
            for row in data:
                results.append(row)

        return {'data': results}


@view_config(route_name='search/results/email', renderer='../templates/search.jinja2')
def email_view(request):
    """Send email after scraper has run at user request."""

    if request.method == 'POST':  # pragma: no cover
        with open('./results.csv') as input_file:
            reader = csv.reader(input_file)
            data = list(reader)
        data.pop(0)
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
    return HTTPFound(location=request.route_url('profile'))


@view_config(route_name='search/results/download')
def download_results(request):
    """Send user their search results as a CSV."""
    response = FileResponse(
        './results.csv',
        request=request,
        content_type='text/csv')
    return response
