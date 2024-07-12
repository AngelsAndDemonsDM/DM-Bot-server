import argparse
import asyncio
import logging
import os
import platform
import subprocess
import sys

from api.auth import auth_bp
from quart import Quart, jsonify
from systems.auto_updater import needs_update
from systems.db_manager import SettingsManager

app = Quart(__name__)

# Blueprint
app.register_blueprint(auth_bp, url_predix='/auth')

# Status resp
@app.route('/status', methods=['GET'])
async def get_status():
    return jsonify({"message": "Service is running"}), 200

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
    
    if asyncio.run(SettingsManager().get_setting("app.auto_update")):
        if needs_update():
            logging.info("Updating application...")
            run_file_in_new_console(os.path.join("Code", "auto_updater", "auto_updater.py"))
            sys.exit(0)

    app.run(debug=debug)
