from flask import Blueprint, render_template

error_pages_bp = Blueprint('errors', __name__, static_folder='web')


@error_pages_bp.app_errorhandler(401)
def unauthorized_error(error):
    return render_template('error_pages/401.html'), 401

@error_pages_bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('error_pages/404.html'), 404

@error_pages_bp.app_errorhandler(500)
def internal_error(error):
    return render_template('error_pages/500.html'), 500
