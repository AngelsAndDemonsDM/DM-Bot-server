import argparse
import logging
import os
import platform
import subprocess
import sys
from logging.config import dictConfig
from threading import Thread
from typing import Tuple

from api import *
from quart import Quart
from quart.logging import default_handler
from systems.auto_updater import AutoUpdater
from systems.db_systems import MainSettings
from systems.events_system import EventManager, events

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

def register_events() -> None:
    logger = logging.getLogger("Event manager")
    logger.info("Start register events")
    
    ev_manager: EventManager = EventManager.get_instance()
    event_names = events.__all__
    
    for name in event_names:
        handler = getattr(events, name)
        
        if callable(handler) and hasattr(handler, 'event_name'):
            event_name = handler.event_name
            ev_manager.register_event(event_name, handler)
            logger.info(f"Registered event '{event_name}' with handler {handler.__name__}")
    
    logger.info("End register events")

def load_config() -> Tuple[str, int, int, bool]:
    logger = logging.getLogger("Settings manager")
    logger.info("Start load settings")
    
    host: str = "127.0.0.1"
    port: int = 5000
    socket_port: int = 5001
    auto_update: bool = False
    
    with MainSettings.get_instance() as config:
        config: MainSettings
        if not config.initialize_default_settings({
                "app.auto_git_update": False,
                "server.ip": "127.0.0.1",
                "server.http_port": 5000,
                "server.socket_port": 5001,
            }):
            host = config.get_setting("server.ip")
            port = config.get_setting("server.http_port")
            socket_port = config.get_setting("server.socket_port")
            auto_update = config.get_setting("app.auto_git_update")
            logger.info(f"Config set. ip: {host}, port: {port}, soket port: {socket_port}, auto_update: {auto_update}")
        
        else:
            logger.info(f"Base config set.")
        
    return host, port, socket_port, auto_update

def start_socket(ip: str, port: int):
    server_thread = Thread(target=start_socket_server, args=(ip, port))
    server_thread.start()

# Start program
if __name__ == "__main__":
    args = parse_arguments()
    debug = args.debug

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
            'level': logging.DEBUG if debug else logging.INFO,
            'handlers': ['default'],
        },
    })

    register_events()
    
    host, port, socket_port, auto_update = load_config()

    if auto_update:
        updater = AutoUpdater()
        if updater.is_needs_update():
            run_file_in_new_console(os.path.join("Code", "auto_updater", "auto_updater.py"))
            sys.exit(0)
        
        else:
            del updater
    
    start_socket(host, int(socket_port))

    app.run(host=host, port=int(port), debug=debug)
