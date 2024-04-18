import logging
import os
import subprocess

from changelog import Changelog
from colorlog import ColoredFormatter
from updater import Updater


def clear_consol():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause_consol():
    input("Нажмите Enter для продолжения...")

def show_menu(version) -> int:
    while True:
        clear_consol()
        print("Автоматический лаунчер обновлений для DM-Bot")
        print_table(version, ["Многоликий демон - Код", "Vergrey - Оформление, помощь с кодом"])
        print("Меню выбора:")
        print("1. Обновить программу")
        print("2. Просмотр ченджлога")
        print("3. Запуск программы")
        print("0. Выход")
        choice = input("Введите число: ")
        if choice in {"0", "1", "2", "3"}:
            return int(choice)
        else:
            print("Неверное число. Просьба повторить ввод.")
            pause_consol()

def print_table(version, created_by):
    if not version:
        version = "None"

    max_created_by_length = max(len(item) for item in created_by)
    version_length = len(version)
    top_bottom_line_width = max(version_length, max_created_by_length) + 15
    
    print("*" + "-" * (top_bottom_line_width) + "*")
    print("| Version -", version, " " * (top_bottom_line_width - version_length - 13), "|")
    print("*" + "-" * (top_bottom_line_width) + "*")
    
    for creator in created_by:
        print("| Created by:", creator, " " * (top_bottom_line_width - len(creator) - 15), "|")
    
    print("*" + "-" * (top_bottom_line_width) + "*\n")

def main() -> None:
    update_class = Updater()
    changelog_class = Changelog()
    while True:
        clear_consol()
        menu = show_menu(update_class.version)

        match menu:
            case 1: # Обновить программу
                clear_consol()
                update_class.update()
                pause_consol()
            
            case 2: # Просмотр ченджлога
                clear_consol()
                logging.info("Запрос ченджлога с сервера...")
                
                try:
                    changelog_class.get_changelog()
                    changelog_class.print_changelog()
                except Exception as err:
                    logging.error(f"Произошла ошибка при получении ченджлога: {err}")
                
                pause_consol()
            
            case 3: # Запуск программы
                clear_consol()
            
                if os.path.exists("DM-Bot\\main.exe"):
                    subprocess.Popen("DM-Bot\\main.exe")
                    return
                else:
                    logging.error("Файл программы не обнаружен, просьба обновить программу!")
                    pause_consol()
            
            case 0: # Выход из программы
                return

if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    formatter = ColoredFormatter(
        "[%(asctime)s] [%(log_color)s%(levelname)s%(reset)s] - %(message)s",
        datefmt=None,
        reset=True,
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'purple',
        },
        secondary_log_colors={},
        style='%'
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    main()
