from quart import Blueprint, jsonify, request, send_file
from root_path import ROOT_PATH

connect_bp = Blueprint('connect', __name__)
