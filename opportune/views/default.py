from pyramid.view import view_config
from pyramid.security import NO_PERMISSION_REQUIRED
from ..models import Account
import smtplib
import os
import csv


@view_config(route_name='home', renderer='../templates/index.jinja2',
             permission=NO_PERMISSION_REQUIRED)
def home_view(request):
    """Return homepage."""
    return {}


@view_config(route_name='profile', renderer='../templates/profile.jinja2')
def profile_view(request):
    """Return profile settings page."""
    return {}


@view_config(route_name='about', renderer='../templates/about.jinja2',
             permission=NO_PERMISSION_REQUIRED)
def about_view(request):
    """Return about page."""
    return {}


@view_config(route_name='email', renderer='../templates/email.jinja2')
def email_view(request):
    """Email testing."""
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
