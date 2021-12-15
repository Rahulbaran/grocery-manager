from flask import Blueprint, render_template


handlers = Blueprint('errorbp', __name__)



@handlers.app_errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html', title='Page Not Found'),404




status_codes = [500,413,403]
error_headings = ['Server is Down 📉', 'Entity Too Large', 'Access Forbidden']

@handlers.app_errorhandler(500)
def server_down(e):
    return render_template(
        'errors/error.html',
        title='Server Down',
        code=status_codes[0],
        error_heading = error_headings[0],
        message = 'Our server is not working properly😒 please try again after sometimes🙂'
    ),500



@handlers.app_errorhandler(413)
def too_large(e):
    return render_template(
        'errors/error.html',
        title='Too Large',
        code=status_codes[1],
        error_heading = error_headings[1],
        message = 'You are allowed to upload file of upto 16MB'
    ),413



@handlers.app_errorhandler(403)
def forbidden(e):
    return render_template(
        'errors/error.html',
        title='Forbidden',
        code=status_codes[2],
        error_heading = error_headings[2],
        message = 'You are not allowed to access the requested page🚫'
    ),403