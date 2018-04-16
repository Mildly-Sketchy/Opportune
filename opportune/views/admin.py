@view_config(route_name='analytics', 
    renderer='../templates/admin.jinja2')

def analytics_view(request):
    """Return employer analytics."""
    request.route_url()
    return {}