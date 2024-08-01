import argparse
import asyncio
import logging
import os
import platform
import subprocess
import sys
from logging.config import dictConfig

from systems.auto_updater import AutoUpdater
from systems.db_systems import load_config
from systems.events_system import register_events
from systems.network import SoketServerSystem


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

async def main():
    register_events()
    
    host, port, auto_update = load_config()

    if auto_update:
        updater = AutoUpdater()
        if updater.is_needs_update():
            run_file_in_new_console(os.path.join("Code", "auto_updater", "auto_updater.py"))
            sys.exit(0)
        else:
            del updater
            
    server_system = SoketServerSystem()
    server = await asyncio.start_server(server_system.handle_client, host, int(port))
    logging.info(f"Server started on {host}:{port}")

    async def shutdown():
        logging.info("Shutting down server...")
        server.close()
        await server.wait_closed()
        logging.info("Server shutdown complete")

    try:
        await server.serve_forever()
    
    except asyncio.CancelledError:
        await shutdown()

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
    
    try:
        asyncio.run(main())
    
    except KeyboardInterrupt:
        logging.info("Server shutdown initiated by user.")
