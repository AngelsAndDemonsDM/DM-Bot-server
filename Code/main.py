import argparse
import asyncio
import logging
import os
import platform
import subprocess
import sys
from pathlib import Path

from api import DownloadServerModule, UserServerModule
from DMBotNetwork import Server
from dotenv import load_dotenv
from root_path import ROOT_PATH
from systems.auto_updater import AutoUpdater
from systems.entity_system import EntityFactory
from systems.file_work import MainAppSettings

load_dotenv()


class FixedWidthFormatter(logging.Formatter):
    def format(self, record):
        record.levelname = f"{record.levelname:<7}"
        return super().format(record)


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
    logging.info("Initialize main_app_settings.json...")
    main_settings = MainAppSettings()
    main_settings.init_base_settings(
        {
            "app": {
                "host": "localhost",
                "port": 5000,
                "timeout": 30.0,
                "allow_registration": True,
                "server_name": "dev",
                "max_players": 25,
            }
        }
    )
    logging.info("Done")

    logging.info("Initialize EntityFactory...")
    EntityFactory()  # Singleton moment. Создаём объект для всего проекта
    logging.info("Done")

    logging.info("Initialize Server modules...")
    Server()
    Server.register_methods_from_class([DownloadServerModule, UserServerModule])
    logging.info("Done")


async def main() -> None:
    main_settings = MainAppSettings()

    if main_settings.get_s("app.auto_update"):
        updater = AutoUpdater()
        if updater.is_needs_update():
            run_file_in_new_console(
                ROOT_PATH / "Code" / "auto_updater" / "auto_updater.py"
            )
            sys.exit(0)

        else:
            del updater

    base_access_flags = {
        "change_allow_registration": False,
        "create_users": False,
        "delete_users": False,
        "change_access": False,
        "change_password": True,
    }

    env_password = os.getenv("OWNER_PASSWORD")
    base_owener_password = env_password if env_password else "owner_password"

    await Server.setup_server(
        server_name=main_settings.get_s("app.server_name"),
        host=main_settings.get_s("app.host"),
        port=main_settings.get_s("app.port"),
        db_path=Path(ROOT_PATH / "data"),
        init_owner_password=base_owener_password,
        base_access=base_access_flags,
        allow_registration=main_settings.get_s("app.allow_registration"),
        timeout=main_settings.get_s("app.timeout"),
        max_player=main_settings.get_s("app.max_players"),
    )

    await Server.start()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Запуск сервера DMBot")
    parser.add_argument("--debug", action="store_true", help="Включение режима отладки")

    args = parser.parse_args()

    log_level = logging.DEBUG if args.debug else logging.INFO

    handler = logging.StreamHandler()
    formatter = FixedWidthFormatter(
        "[%(asctime)s][%(levelname)s] %(name)s: %(message)s"
    )

    handler.setFormatter(formatter)

    logging.basicConfig(
        level=log_level,
        handlers=[handler],
    )

    init_all()

    try:
        asyncio.run(main())

    except KeyboardInterrupt:
        logging.info("Server shutdown initiated by user.")
