import argparse
import asyncio
import os

from etc.auto_docs import generate_documentation
from etc.logger import LoggerManager
from modules.organs_main import organs_main
from tests.run_tests import run_tests



def clear_consol():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause_consol():
    input("Нажмите Enter для продолжения...")

def parse_arguments():
    parser = argparse.ArgumentParser(description='DM-Bot')
    parser.add_argument('--debug', action='store_true', help='Включить режим отладки')
    return parser.parse_args()

def show_menu_debug():
    while True:
        clear_consol()
        print("DEBUG MODE!\n")
        print("Меню выбора:")
        print("1. Запуск тестов")
        print("2. Создать документацию")
        print("3. Тест системы органов")
        print("0. Выход")
        choice = input("Введите число: ")
        if choice in {"0", "1", "2", "3"}:
            return int(choice)
        else:
            print("Неверное число. Просьба повторить ввод.")
            pause_consol()

async def main_debug():
    # Объявление менеджеров
    logger = LoggerManager(True)

    # Меню выбора
    while True:
        menu = show_menu_debug()
        
        if menu == 1: # Запуск тестов
            anser = await run_tests(logger)
            if anser:
                logger.info("Все тесты пройдены удачно")
            else:
                logger.error("Один из тестов был провален!")
            pause_consol()
            continue
            
        if menu == 2: # Генерация документации
            generate_documentation(logger)
            pause_consol()
            continue

        if menu == 3: # Тест системы органов
            organs_main()
            continue

        if menu == 0: # Выход из программы
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
        print_table("███", ["Многоликий демон - Код", "Vergrey - Оформление, помощь с кодом"])
        print("А ничего не готово для резил билда.\n")
        print("Меню выбора:")
        print("0. Выход")
        choice = input("Введите число: ")
        if choice in {"0"}:
            return int(choice)
        else:
            print("Неверное число. Просьба повторить ввод.")
            pause_consol()


async def main():
    # Объявление менеджеров
    logger = LoggerManager(False)

    # Меню выбора
    while True:
        menu = show_menu()
        
        if menu == 1: # Запуск тестов
            anser = await run_tests(logger)
            if anser:
                logger.info("Все тесты пройдены удачно")
            else:
                logger.error("Один из тестов был провален!")
            pause_consol()
            continue
            
        if menu == 2: # Генерация документации
            generate_documentation(logger)
            pause_consol()
            continue

        if menu == 3: # Тест системы органов
            organs_main()
            continue

        if menu == 0: # Выход из программы
            return


if __name__ == "__main__":
    args = parse_arguments()
    debug = args.debug
    if debug:  
        asyncio.run(main_debug())
    else:
        asyncio.run(main())