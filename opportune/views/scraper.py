import requests
import bs4
from bs4 import BeautifulSoup
import urllib3
import pandas as pd
from pyramid.view import view_config


@view_config(route_name='jobs', renderer='../templates/email.jinja2')
def get_jobs(request):
    if request.method == 'POST':
        city = request.POST['city']
        jobs = request.POST['keyword']

        url_template = 'https://www.indeed.com/jobs?q={}&l={}'
        max_results_per_city = 10

        df = pd.DataFrame(columns=['location', 'company', 'job_title', 'salary', 'job_link'])
        requests.packages.urllib3.disable_warnings()
        for job in jobs:
            for start in range(0, max_results_per_city):
                url = url_template.format(job, city)
                http = urllib3.PoolManager()
                response = http.request('GET', url)
                soups = BeautifulSoup(response.data.decode('utf-8'), 'html5lib')
                for b in soups.find_all('div', attrs={'class': ' row result'}):
                    location = b.find('span', attrs={'class': 'location'}).text
                    job_title = b.find('a', attrs={'data-tn-element': 'jobTitle'}).text
                    base_url = 'http://www.indeed.com'
                    href = b.find('a').get('href')
                    job_link = f'{base_url}{href}'
                    try:
                        company = b.find('span', attrs={'class': 'company'}).text
                    except:
                        company = 'NA'
                    try:
                        salary = b.find('span', attrs={'class': 'no-wrap'}).text
                    except:
                        salary = 'Not Listed'
                    df = df.append({'location': location, 'company': company, 'job_title': job_title, 'salary': salary, 'job_link': job_link}, ignore_index=True)

        df.company.replace(regex=True,inplace=True,to_replace='\n',value='')
        df.salary.replace(regex=True,inplace=True,to_replace='\n',value='')
        df.salary.replace(regex=True, inplace=True, to_replace='\$', value='')
        output = df.head(20)
        output.to_csv('results.csv', index=False)
        return {}
