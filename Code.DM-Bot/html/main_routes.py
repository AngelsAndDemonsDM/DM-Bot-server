from flask import Blueprint
from .pages.about import about
from .pages.bot import bot_main_page
from .pages.index import index

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home_page():
    return index()

@main_bp.route("/bot")
def bot_page():
    return bot_main_page()

@main_bp.route('/about')
def about_page():
    return about()
