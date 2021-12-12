from flask import Blueprint, render_template



handlers = Blueprint('errorbp', __name__)



@handlers.app_errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html', title='Page Not Found'),404