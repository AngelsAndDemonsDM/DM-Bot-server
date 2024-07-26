import argparse
import logging
import os
import platform
import subprocess
import sys
from logging.config import dictConfig
from threading import Thread

from api import *
from quart import Quart
from quart.logging import default_handler
from systems.auto_updater import AutoUpdater
from systems.db_systems import SettingsManager
from systems.events_system import register_ev

app = Quart(__name__)
app.logger.removeHandler(default_handler)

# Blueprint
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(server_bp, url_prefix='/server')

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

def start_socket(ip: str, port: int):
    server_thread = Thread(target=start_socket_server, args=(ip, port))
    server_thread.start()

# Start program
if __name__ == "__main__":
    args = parse_arguments()
    debug = args.debug

    # Настройка логирования
    log_level = logging.DEBUG if debug else logging.INFO

    # Базовая конфигурация логгера
    dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                'format': '[%(asctime)s] [%(levelname)s] %(name)s: %(message)s',
            },
        },
        'handlers': {
            'default': {
                'class': 'logging.StreamHandler',
                'formatter': 'default',
            },
        },
        'root': {
            'level': log_level,
            'handlers': ['default'],
        },
    })

    ip = ""
    port = ""
    soket_port = ""
    
    register_ev()
    
    with SettingsManager() as config:
        if config.get_setting('app.auto_update', False):
            updater = AutoUpdater()
            if updater.is_needs_update():
                run_file_in_new_console(os.path.join("Code", "auto_updater", "auto_updater.py"))
                sys.exit(0)
        
        ip = config.get_setting('server.ip', "127.0.0.1") 
        port = config.get_setting('server.port', 5000)
        soket_port = config.get_setting('server.ip', 5001)
    
    start_socket(ip, int(soket_port))

    app.run(host= ip, port=int(port), debug=debug)
