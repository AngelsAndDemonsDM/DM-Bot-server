from flask import Blueprint

from .pages import about_main_page, bot_main_page, index_main_page

main_bp = Blueprint('main', __name__)

# Главное окно приложения
@main_bp.route('/')
def home_page():
    return index_main_page()

# Окно с управлением ботом 
@main_bp.route("/bot")
def bot_page():
    return bot_main_page()

# О говнюках =)
@main_bp.route('/about')
def about_page():
    return about_main_page()
