import tempfile

import requests
import yaml
from requests.exceptions import RequestException
from server_info import ServerInfo


class Changelog(ServerInfo):
    def __init__(self) -> None:
        """
        Инициализация объекта класса Changelog.
        Вызывает конструктор родительского класса ServerInfo.
        """
        super().__init__()
    
    def get_changelog(self) -> dict:
        """
        Получает changelog с сервера и возвращает его в формате словаря.

        Raises:
            ValueError: Если 'changelog_id' отсутствует в _info_json.
            RequestException: Если возникает ошибка при загрузке changelog.

        Returns:
            dict: Словарь с информацией из changelog.
        """
        if 'changelog_id' not in self._info_json:
            raise ValueError("\"changelog_id\" not found on server")
        
        response = requests.get(self._url(self._info_json['changelog_id']), stream=True)
        if response.status_code == 200:
            with tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as temp_file:
                for line in response.iter_lines(decode_unicode=True):
                    if line:
                        temp_file.write(line + '\n')
                temp_filename = temp_file.name
            
            with open(temp_filename, 'r', encoding='utf-8') as file:
                changelog_text = file.read()
            
            changelog_data = yaml.safe_load(changelog_text)
            return changelog_data
        else:
            raise RequestException("Error when downloading changelog")

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
        changelog_info = self.get_changelog()
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
