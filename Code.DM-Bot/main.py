import argparse
import asyncio
import logging
import os
import sys

from colorlog import ColoredFormatter
from etc.auto_docs import generate_documentation
from main_vars import VERSION
from tests.run_tests import run_tests


def clear_consol():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause_consol():
    input("Нажмите Enter для продолжения...")

def parse_arguments():
    parser = argparse.ArgumentParser(description='DM-Bot')
    parser.add_argument('--debug', action='store_true', help='Включить режим отладки')
    parser.add_argument('--version', action='store_true', help='Возвращает версию приложения')
    return parser.parse_args()

def show_menu_debug():
    while True:
        clear_consol()
        print("DEBUG MODE!\n")
        print("Меню выбора:")
        print("1. Запуск тестов")
        print("2. Создать документацию")
        print("0. Выход")
        choice = input("Введите число: ")
        if choice in {"0", "1", "2"}:
            return int(choice)
        else:
            print("Неверное число. Просьба повторить ввод.")
            pause_consol()

async def main_debug():
    # Меню выбора
    while True:
        menu = show_menu_debug()
        
        match menu:
            case 1: # Запуск тестов
                run_tests()
                pause_consol()
            case 2: # Генерация документации
                generate_documentation()
                pause_consol()
            case 0: # Выход из программы
                return


def print_table(version, created_by):
    max_created_by_length = max(len(item) for item in created_by)
    version_length = len(version)
    top_bottom_line_width = max(version_length, max_created_by_length) + 15
    print("*" + "-" * (top_bottom_line_width) + "*")
    print("| Version -", version, " " * (top_bottom_line_width - version_length - 13), "|")
    print("*" + "-" * (top_bottom_line_width) + "*")
    for creator in created_by:
        print("| Created by:", creator, " " * (top_bottom_line_width - len(creator) - 15), "|")
    print("*" + "-" * (top_bottom_line_width) + "*\n")

def show_menu():
    while True:
        clear_consol()
        print_table(VERSION, ["Многоликий демон - Код", "Vergrey - Оформление, помощь с кодом"])
        print("Меню выбора:")
        print("0. Выход")
        choice = input("Введите число: ")
        if choice in {"0"}:
            return int(choice)
        else:
            print("Неверное число. Просьба повторить ввод.")
            pause_consol()


async def main():
    # Меню выбора
    while True:
        menu = show_menu()
        
        match menu:
            case 0: # Выход из программы
                return


if __name__ == "__main__":
    args = parse_arguments()
    version = args.version
    if version:
        print(VERSION)
        sys.exit()
    
    debug = args.debug

    logger = logging.getLogger()
    if debug:
        logger.setLevel(logging.DEBUG)        
    else:
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

    if debug:
        asyncio.run(main_debug())
    else:
        asyncio.run(main())