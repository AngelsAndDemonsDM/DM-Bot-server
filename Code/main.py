import argparse
import asyncio
import logging
import platform
import subprocess
import sys
from logging.config import dictConfig
from pathlib import Path

from api import *
from DMBotNetwork import Server
from root_path import ROOT_PATH
from systems.auto_updater import AutoUpdater
from systems.entity_system import EntityFactory
from systems.file_work import MainAppSettings


# Argument parsing
def parse_arguments():
    parser = argparse.ArgumentParser(description='DM-Bot')
    parser.add_argument('--debug', action='store_true', help='Включить режим отладки')
    return parser.parse_args()

# Function to run a file in a new console
def run_file_in_new_console(file_path: Path) -> None:
    absolute_path = file_path.resolve()
    system = platform.system()
    
    if system == "Windows":
        subprocess.Popen(["start", "cmd", "/c", f"python {absolute_path}"], shell=True)
    
    elif system == "Darwin":
        subprocess.Popen(["open", "-a", "Terminal", str(absolute_path)])
    
    else:
        subprocess.Popen(["x-terminal-emulator", "-e", f"python {absolute_path}"])

def init_all() -> None:
    logging.info("Initialize base server access...")
    Server.BASE_ACCESS = {
        "create_users": False,
        "delete_users": False,
        "change_access": False,
        "change_password": True
    }
    logging.info("Done")
    
    logging.info("Initialize main_app_settings.json...")
    main_settings = MainAppSettings()
    main_settings.init_base_settings({
        "app": {
            "host": "localhost",
            "port": 5000,
            "auto_update": False,
            "db_path": "data"
        }
    })
    logging.info("Done")
    
    logging.info("Initialize EntityFactory...")
    EntityFactory() # Singleton moment. Создаём объект для всего проекта
    logging.info("Done")
    
async def main() -> None:
    main_settings = MainAppSettings()
    
    if main_settings.get_s("app.auto_update"):
        updater = AutoUpdater()
        if updater.is_needs_update():
            run_file_in_new_console(ROOT_PATH / "Code" / "auto_updater" / "auto_updater.py")
            sys.exit(0)
        
        else:
            del updater

    db_path = ROOT_PATH / Path(main_settings.get_s("app.db_path"))
    host = main_settings.get_s("app.host")
    port = main_settings.get_s("app.port")
    
    server = Server(host=host, port=port, db_path=db_path)

    await server.start()

if __name__ == "__main__":
    args = parse_arguments()
    debug = args.debug

    # Базовая конфигурация логгера
    dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                'format': '[%(asctime)s]-[%(levelname)s] \"%(name)s\": %(message)s',
            },
        },
        'handlers': {
            'default': {
                'class': 'logging.StreamHandler',
                'formatter': 'default',
                'stream': 'ext://sys.stdout',
            },
        },
        'root': {
            'level': logging.DEBUG if debug else logging.INFO,
            'handlers': ['default'],
        },
    })
    
    init_all()
    
    try:
        asyncio.run(main())
    
    except KeyboardInterrupt:
        logging.info("Server shutdown initiated by user.")
