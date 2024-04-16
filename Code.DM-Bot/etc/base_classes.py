class BaseObject:
    def __init__(self, id: str, name: str, description: str) -> None:
        """
        Инициализация класса базового объекта. Включает в себя базовую логику работы с базовыми переменными

        Attributes:
            id (str): ID объекта
            name (str): Имя объекта
            description (str): Описание объекта
        """
        self._id: str = id
        self._name: str = name
        self._description: str = description
    
    # get metods
    @property
    def id(self) -> str:
        """
        Публичное поле id объекта

        Является одновременно сеттером и геттером
        """
        return self._id
    
    @property
    def name(self) -> str:
        """
        Публичное поле name объекта

        Является одновременно сеттером и геттером
        """
        return self._name

    @property
    def description(self) -> str:
        """
        Публичное поле description объекта

        Является одновременно сеттером и геттером
        """
        return self._description

    # set metods
    @id.setter
    def id(self, value: str):
        self._id = value

    @name.setter
    def name(self, value: str):
        self._name = value

    @description.setter
    def description(self, value: str):
        self._description = value
