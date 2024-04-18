from flask import Blueprint

from .pages.about import about
from .pages.bot import bot_main_page
from .pages.index import index

main_bp = Blueprint('main', __name__)

# Главное окно приложения
@main_bp.route('/')
def home_page():
    return index()

# Окно с управлением ботом 
@main_bp.route("/bot")
def bot_page():
    return bot_main_page()

# О говнюках =)
@main_bp.route('/about')
def about_page():
    return about()
