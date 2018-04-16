from pyramid.view import view_config


@view_config(route_name='home', renderer='../templates/index.jinja2')
def home_view(request):
    """Return homepage."""
    return {}


@view_config(route_name='login', renderer='../templates/login.jinja2')
def login_view(request):
    """Return login page."""
    return {}


@view_config(route_name='register', renderer='../templates/register.jinja2')
def register_view(request):
    """Return registration page."""
    return {}


@view_config(route_name='profile', renderer='../templates/profile.jinja2')
def profile_view(request):
    """Return profile settings page."""
    return {}


@view_config(route_name='analytics', renderer='../templates/admin.jinja2')
def analytics_view(request):
    """Return employer analytics."""
    return {}


@view_config(route_name='about', renderer='../templates/about.jinja2')
def about_view(request):
    """Return about page."""
    return {}
