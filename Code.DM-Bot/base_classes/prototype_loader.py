import os
from abc import ABC, abstractmethod

import yaml


class PrototypeLoader(ABC):
    def __init__(self, file_path, type: str = None):
        """
        Инициализатор класса PrototypeLoader.

        Args:
            file_path (str): Путь к каталогу с прототипами.
            type (str, optional): Тип прототипа для загрузки. Если не указан, вызывается исключение.

        Raises:
            NotImplementedError: Если тип прототипа не указан.
        """
        directory_path = os.path.join(os.getcwd(), 'Prototype.DM-Bot', file_path)

        if type is None:
            raise NotImplementedError(f"{self.__class__.__name__} does not have an established prototype type to read")
        self._type = type.lower()
        
        self._id_set = set()
        self._prototypes = self._load_prototypes(directory_path)

    def _load_prototypes(self, directory_path):
        """
        Загружает прототипы из файлов в указанной директории.

        Args:
            directory_path (str): Путь к директории с файлами прототипов.

        Returns:
            list: Список загруженных прототипов.

        Raises:
            ValueError: Если найдены дубликаты ID прототипов.
            TypeError: Если невозможно вызвать функцию создания прототипа.
        """
        prototypes_list = []

        for root, dirs, files in os.walk(directory_path):
            for file_name in files:
                if file_name.endswith('.yml'):
                    file_path = os.path.join(root, file_name)
                    with open(file_path, 'r', encoding='utf-8') as file:
                        prototypes_config = yaml.safe_load(file)

                        for config in prototypes_config:
                            if str(config.get('type')).lower() != self._type:
                                continue

                            creator_func = self._get_func(config)

                            if creator_func:
                                proto = creator_func(config)
                                if proto.id in self._id_set:
                                    raise ValueError(f"Duplicate id '{proto.id}' found.")
                                prototypes_list.append(proto)
                                self._id_set.add(proto.id)
                            else:
                                raise TypeError(f"Cannot call function {creator_func} in '{self.__class__.__name__}'")

        return prototypes_list
    
    @abstractmethod
    def _get_func(self, config):
        """
        Возвращает функцию для создания прототипа. Этот метод должен быть переопределён в дочерних классах.

        Args:
            config (dict): Конфигурация прототипа.

        Raises:
            NotImplementedError: Если метод не переопределён.
        """
        pass

    def _validate_config_param(self, config, param_name, id="Unknown prototype"):
        """
        Проверяет наличие и возвращает значение указанного параметра в конфигурации прототипа.

        Args:
            config (dict): Конфигурация прототипа.
            param_name (str): Имя параметра для проверки.
            id (str, optional): Идентификатор прототипа. Используется для сообщений об ошибках.

        Returns:
            Any: Значение параметра.

        Raises:
            ValueError: Если параметр отсутствует в конфигурации.
        """
        param_value = config.get(param_name)

        if param_value is None:
            raise ValueError(f"Parameter '{param_name}' is missing in the prototype: '{id}'.")
        
        return param_value

    def __getitem__(self, key: str):
        """
        Возвращает прототип по его идентификатору.

        Args:
            key (str): Идентификатор прототипа.

        Returns:
            Prototype or None: Возвращает прототип, если найден; в противном случае возвращает None.
        """
        for prototype in self._prototypes:
            if prototype.id == key:
                return prototype
        
        return None

    @property
    def prototypes(self) -> list:
        """
        Свойство для получения списка всех прототипов.

        Returns:
            list: Список прототипов.
        """
        return self._prototypes
