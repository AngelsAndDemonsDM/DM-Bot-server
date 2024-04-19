import logging
import os
import subprocess

from colorlog import ColoredFormatter

from . import Changelog, Updater


def clear_consol():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause_consol():
    input("Нажмите Enter для продолжения...")

def show_menu(version) -> int:
    while True:
        clear_consol()
        
        print_table(version, ["Многоликий демон - Код", "Vergrey - Оформление, помощь с кодом"])
        print("Меню выбора:\n")
        print("1. Обновить программу")
        print("2. Просмотр ченджлога")
        print("3. Запуск программы")
        print("0. Выход\n\n")
        choice = input("Введите число: ")
        if choice in {"0", "1", "2", "3"}:
            return int(choice)
        else:
            print("Неверное число. Просьба повторить ввод.")
            pause_consol()

def print_table(version, created_by):
    if not version:
        version = "None"
    # Именованные константы для заголовка, маржи, меток версии и создателей
    HEADER_TITLE = "Автоматический лаунчер обновлений для DM-Bot"
    HEADER_MARGIN = 4
    VERSION_LABEL = "Version -"
    CREATED_BY_LABEL = "Created by:"

    # Вычисляем длины
    max_created_by_length = max(len(item) + len("Created by:") for item in created_by)
    version_length = len(version)
    const_length = len(HEADER_TITLE)
    
    # Вычисляем ширину верхней и нижней линий
    top_bottom_line_width = max(version_length, max_created_by_length, const_length) + 2 * HEADER_MARGIN
    
    # Выводим заголовок
    print("┌" + "─" * top_bottom_line_width + "┐")
    print(f"│ {HEADER_TITLE}{' ' * (top_bottom_line_width - const_length - 2)} │")
    print("├" + "─" * top_bottom_line_width + "┤")
    
    # Выводим версию
    version_line = f"│ {VERSION_LABEL} {version}{' ' * (top_bottom_line_width - version_length - len(VERSION_LABEL) - 3)} │"
    print(version_line)
    print("├" + "─" * top_bottom_line_width + "┤")
    
    # Выводим создателей
    for creator in created_by:
        creator_line = f"│ {CREATED_BY_LABEL} {creator}{' ' * (top_bottom_line_width - len(creator) - len(CREATED_BY_LABEL) - 3)} │"
        print(creator_line)
    
    # Выводим нижнюю линию
    print("└" + "─" * top_bottom_line_width + "┘")


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
                print()
                try:
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
