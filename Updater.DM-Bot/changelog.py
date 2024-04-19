import logging
import os

import requests
import yaml
from requests.exceptions import RequestException

from . import ServerInfo


class Changelog(ServerInfo):
    def __init__(self) -> None:
        """
        Инициализация объекта класса Changelog.
        Вызывает конструктор родительского класса ServerInfo.
        """
        super().__init__()
    
    def download_changelog(self, file_name="changelog.yaml", chunk_size=8192, retries=3, timeout=30):
        """
        Скачивает ченджлог с сервера.

        Args:
            file_name (str): Имя файла для сохранения ченджлога.
            chunk_size (int): Размер части для скачивания.
            retries (int): Количество попыток скачивания.
            timeout (int): Время ожидания ответа сервера.

        Raises:
            RequestException: Если скачивание ченджлога не удалось после всех попыток.

        Returns:
            str: Имя скачанного файла ченджлога.
        """
        if 'changelog_id' not in self._info_json:
            raise ValueError("\"changelog_id\" not found in json_data")
        
        for _ in range(retries):
            try:
                with requests.get(self._url(self._info_json['changelog_id']), stream=True, timeout=timeout) as response:
                    response.raise_for_status()
                    
                    with open(file_name, 'wb') as file:
                        for chunk in response.iter_content(chunk_size=chunk_size):
                            if chunk:
                                file.write(chunk)
                
                return file_name
            
            except requests.Timeout:
                print(f"Timeout occurred during changelog download. Retrying ({retries} retries left).")
            except requests.RequestException as e:
                print(f"Error during changelog download: {e}. Retrying ({retries} retries left).")
        
        raise RequestException(f"Failed to download changelog after {retries} retries.")

    def print_changelog(self) -> None:
        """
        Выводит changelog на экран, разбивая на страницы по 10 версий.
        
        Выводит информацию о версиях, датах и изменениях в формате:
            Версия: [version]
            Дата: [date]
            Изменения:
                - [change1]
                - [change2]
                ...
        
        Если changelog отсутствует или пользователь решит не продолжать просмотр,
        выводится соответствующее сообщение.
        """
        try:
            file_name = self.download_changelog()
            with open(file_name, 'r', encoding='utf-8') as file:
                changelog_data = yaml.safe_load(file)
            
            changelog_list = changelog_data.get('changelog', [])
            
            if not changelog_list:
                logging.error("Не найдено изменений в ченджлоге")
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
                    
                    print("─" * 40)
                
                if end_index < total_versions:
                    choice = input("Хотите продолжить просмотр? (да/нет): ")
                    if choice.lower() != "да":
                        break
                
                start_index += 10

        except Exception as e:
            logging.error(f"Ошибка при выводе ченджлога: {e}")
        finally:
            if os.path.exists(file_name):
                os.remove(file_name)
