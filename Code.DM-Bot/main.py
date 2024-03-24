import argparse
import asyncio
import os

from etc.auto_docs import generate_documentation
from etc.logger import LoggerManager
from tests.run_tests import run_tests


def parse_arguments():
    parser = argparse.ArgumentParser(description='DM-Bot')
    parser.add_argument('--debug', action='store_true', help='Включить режим отладки')
    return parser.parse_args()

def show_menu():
    while True:
        clear_consol()
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

def clear_consol():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause_consol():
    input("Нажмите Enter для продолжения...")

async def main():
    args = parse_arguments()
    debug = args.debug

    # Объявление менеджеров
    logger = LoggerManager(debug)

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
        
        if menu == 0: # Выход из программы
            return

if __name__ == "__main__":
    asyncio.run(main())
