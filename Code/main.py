import argparse
import logging
import os
import platform
import subprocess
import sys

from api import (admin_bp, api_change_access, api_change_password,
                 api_check_status, api_connect, api_delete_user,
                 api_download_server_content, api_login, api_logout,
                 api_register, auth_bp, connect_bp, server_bp)
from quart import Quart
from systems.auto_updater import AutoUpdater
from systems.db_systems import SettingsManager

app = Quart(__name__)

# Blueprint
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(server_bp, url_prefix='/server')

app.register_blueprint(connect_bp)

# Argument parsing
def parse_arguments():
    parser = argparse.ArgumentParser(description='DM-Bot')
    parser.add_argument('--debug', action='store_true', help='Включить режим отладки')
    return parser.parse_args()

# Function to run a file in a new console
def run_file_in_new_console(file_path):
    absolute_path = os.path.abspath(file_path)
    system = platform.system()
    
    if system == "Windows":
        subprocess.Popen(["start", "cmd", "/c", f"python {absolute_path}"], shell=True)
    
    elif system == "Darwin":
        subprocess.Popen(["open", "-a", "Terminal", absolute_path])
    
    else:
        subprocess.Popen(["x-terminal-emulator", "-e", f"python {absolute_path}"])

# Start program
if __name__ == "__main__":
    args = parse_arguments()
    debug = args.debug

    logger = logging.getLogger()
    if debug:
        logger.setLevel(logging.DEBUG)
    
    else:
        logger.setLevel(logging.INFO)
    
    with SettingsManager() as config:
        if config.get_setting('app.auto_update'):
            updater = AutoUpdater()
            if updater.is_needs_update():
                run_file_in_new_console(os.path.join("Code", "auto_updater", "auto_updater.py"))
                sys.exit(0)

    app.run(debug=debug)
