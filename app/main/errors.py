from flask import render_template
from . import main


@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html', msg=e)


@main.app_errorhandler(500)
def server_internal_error(e):
    return render_template('500.html', msg=e)

@main.app_errorhandler(403)
def forbidden_http_erro(e):
    return render_template('403.html', msg=e)