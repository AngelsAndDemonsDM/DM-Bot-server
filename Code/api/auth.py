from quart import Blueprint, jsonify, request, send_file
from root_path import ROOT_PATH

auth_bp = Blueprint('auth', __name__)