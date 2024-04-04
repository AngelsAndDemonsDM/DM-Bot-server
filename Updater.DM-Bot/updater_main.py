import logging
import os
import subprocess
import zipfile

from changelog import Changelog
from colorlog import ColoredFormatter
from updater import Updater


def check_file_in_directory(directory, filename):
    """
    Проверяет наличие файла в директории.
    """
    file_path = os.path.join(directory, filename)
    if os.path.exists(file_path):
        return True
    return False


def check_or_create_directory(directory):
    """
    Проверяет наличие директории.
    Если директория не существует, создает ее.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)


def clear_consol():
    os.system('cls' if os.name == 'nt' else 'clear')


def get_version(directory: str = "DM-Bot", filename: str = "DM-Bot.exe") -> str:
    version: str = "0.0.-1"
    check_or_create_directory(directory)
    if check_file_in_directory(directory, filename):
        result = subprocess.run([f"{directory}/{filename}", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.strip()
    return version


def main() -> None:
    while True:
        clear_consol()
        menu = show_menu()

        if menu == 1:
            clear_consol()
            update()
            pause_consol()
            continue

        if menu == 2:
            clear_consol()
            logging.info("Запрос ченджлога с сервера...")
            cl = Changelog()
            try:
                cl_data = cl.get_changelog()
            except Exception as err:
                logging.error(f"Произошла ошибка при получении ченджлога: {err}")
            print_changelog(cl_data)
            pause_consol()
            continue

        if menu == 0:
            return


def pause_consol():
    input("Нажмите Enter для продолжения...")


def print_changelog(changelog_info):
    changelog_list = changelog_info.get('changelog', [])
    if not changelog_list:
        print("Не найдено изменений в ченджлоге")
        return

    total_versions = len(changelog_list)
    start_index = 0
    while start_index < total_versions:
        end_index = min(start_index + 10, total_versions)
        for version_info in changelog_list[start_index:end_index]:
            version = version_info.get('version', '█.█.█')
            date = version_info.get('date', '████-██-██')
            changes = version_info.get('changes', [])
            print(f"Версия: {version}")
            print(f"Дата: {date}")
            print("Изменения:")
            for change in changes:
                print(f"  - {change}")
            print()
        if end_index < total_versions:
            choice = input("Хотите продолжить просмотр? (да/нет): ")
            if choice.lower() != "да":
                break
        start_index += 10


def show_menu() -> int:
    while True:
        clear_consol()
        version = get_version()
        print("Автоматический лаунчер обновлений для DM-Bot")
        print_table(version, ["Многоликий демон - Код", "Vergrey - Оформление, помощь с кодом"])
        print("Меню выбора:")
        print("1. Обновить программу")
        print("2. Просмотр ченджлога")
        print("0. Выход")
        choice = input("Введите число: ")
        if choice in {"0", "1", "2"}:
            return int(choice)
        else:
            print("Неверное число. Просьба повторить ввод.")
            pause_consol()


def update() -> None:
    directory = "DM-Bot"
    exe_filename = "DM-Bot.exe"
    zip_filename = "DM-Bot.zip"

    version = get_version()
    logging.info(f"Текущая версия приложения {version}.")

    updater = Updater(version)
    try:
        is_new: bool = updater.is_new_version()
    except Exception as err:
        logging.error(f"Получена ошибка при попытке считать новую версию с сервера: {err}")
        return

    if not is_new:
        logging.info("Обновлений не обнаружено. У вас самая новая версия DM-Bot.")
        return

    try:
        logging.info("Начинаю скачивать зашифрованный архив с сервера...")
        encrypted_zip_content = updater.download_new_exe()

        encrypted_zip_path = os.path.join(directory, zip_filename)
        with open(encrypted_zip_path, 'wb') as zip_file:
            zip_file.write(encrypted_zip_content)
        logging.info("Архив сохранён!")

        logging.info("Удаление старого файла DM-Bot.exe")
        os.remove(exe_filename)
         
        logging.info("Начало распаковки...")
        with zipfile.ZipFile(encrypted_zip_path, 'r') as zip_ref:
            zip_ref.extractall(directory, pwd=b"1Ei2ttDIBadNmDHqh3HRIWpipnxh7DwNM")

        logging.info("Архив распакован!")
        os.remove(encrypted_zip_path)

        logging.info("Файл DM-Bot.exe успешно обновлен.")
    except Exception as err:
        logging.error(f"Получена ошибка при попытке обновления: {err}")
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
