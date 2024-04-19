from flask import render_template


def index_main_page():
    return render_template('index.html')