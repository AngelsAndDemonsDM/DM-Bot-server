class OrganBase:
    def __init__(self, id: str, name: str, description: str, max_health: int, standart_efficiency: int, subtype: str = None):
        """
        Инициализирует объект класса OrganBase.

        Args:
            id (str): Уникальный идентификатор органа.
            name (str): Название органа.
            description (str): Описание органа.
            max_health (int): Максимальное значение здоровья органа.
            standart_efficiency (int): Стандартная эффективность работы органа.
            subtype (str, optional): Подтип органа. По умолчанию None.
        """
        self._subtype = subtype
        self._id = id
        self._name = name
        self._description = description
        self._max_health = max_health
        self._standart_efficiency = standart_efficiency
        
        self._efficiency_per_health = standart_efficiency / max_health
        self._health = max_health
        self._efficiency = standart_efficiency
    
    def __new__(cls, *args, **kwargs):
        """
        Метод для создания экземпляра класса.

        Raises:
            NotImplementedError: Вызывается, если пытаются создать экземпляр абстрактного класса.
        """
        if cls is OrganBase:
            raise NotImplementedError(f"You cannot create an abstract '{cls.__class__.__name__}' class. Use inheritance")
        return super().__new__(cls)
    
    def __str__(self):
        """
        Возвращает строковое представление объекта.

        Returns:
            str: Строковое представление объекта.
        """
        return f"subtype: {self._subtype}; id: {self._id}; name: {self._name}; desc: {self._description}; max_health: {self._max_health}; standart_efficiency: {self._standart_efficiency}; efficiency_per_health: {self._efficiency_per_health}; health: {self._health}; efficiency: {self._efficiency}"

    # Get medotds
    @property
    def subtype(self) -> str:
        """
        Возвращает подтип органа.

        Returns:
            str: Подтип органа.
        """
        return self._subtype

    @property
    def id(self) -> str:
        """
        Возвращает уникальный идентификатор органа.

        Returns:
            str: Уникальный идентификатор органа.
        """
        return self._id
    
    @property
    def name(self) -> str:
        """
        Возвращает название органа.

        Returns:
            str: Название органа.
        """
        return self._name
    
    @property
    def description(self) -> str:
        """
        Возвращает описание органа.

        Returns:
            str: Описание органа.
        """
        return self._description

    @property
    def max_health(self) -> int:
        """
        Возвращает максимальное значение здоровья органа.

        Returns:
            int: Максимальное значение здоровья органа.
        """
        return self._max_health
    
    @property
    def standart_efficiency(self) -> int:
        """
        Возвращает стандартную эффективность работы органа.

        Returns:
            int: Стандартная эффективность работы органа.
        """
        return self._standart_efficiency
    
    @property
    def efficiency_per_health(self) -> int:
        """
        Возвращает эффективность работы органа в зависимости от здоровья.

        Returns:
            int: Эффективность работы органа в зависимости от здоровья.
        """
        return self._efficiency_per_health
    
    @property
    def health(self) -> int:
        """
        Возвращает текущее значение здоровья органа.

        Returns:
            int: Текущее значение здоровья органа.
        """
        return self._health
    
    @property
    def efficiency(self) -> int:
        """
        Возвращает текущую эффективность работы органа.

        Returns:
            int: Текущая эффективность работы органа.
        """
        return self._efficiency
    
    # Set medotds
    @subtype.setter
    def subtype(self, value: str):
        """
        Устанавливает подтип органа.

        Args:
            value (str): Подтип органа.
        """
        self._subtype = value

    @id.setter
    def id(self, value: str):
        """
        Устанавливает уникальный идентификатор органа.

        Args:
            value (str): Уникальный идентификатор органа.
        """
        self._id = value
    
    @name.setter
    def name(self, value: str):
        """
        Устанавливает название органа.

        Args:
            value (str): Название органа.
        """
        self._name = value

    @description.setter
    def description(self, value: str):
        """
        Устанавливает описание органа.

        Args:
            value (str): Описание органа.
        """
        self._description = value

    @max_health.setter
    def max_health(self, value: int):
        """
        Устанавливает максимальное значение здоровья органа.

        Args:
            value (int): Максимальное значение здоровья органа.
        """
        self._max_health = value

    @standart_efficiency.setter
    def standart_efficiency(self, value: int):
        """
        Устанавливает стандартную эффективность работы органа.

        Args:
            value (int): Стандартная эффективность работы органа.
        """
        self._standart_efficiency = value
    
    # Methods
    def delta_health(self, delta_health: int):
        """
        Изменяет значение здоровья органа и его эффективность.

        Args:
            delta_health (int): Изменение значения здоровья органа.
        """
        self._health += delta_health
        self._efficiency = self._efficiency_per_health * self._health
