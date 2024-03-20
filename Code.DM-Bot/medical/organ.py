class OrgansSystem:
    def __init__(self):
        self.brain
        self.heart
        self.liver
        self.kidney
        self.lungs
        self.stomach

class Organ:
    def __init__(self):
        self.name
        self.description
        self.health
        self.max_health
        self.standart_efficiency
    
    def __new__(cls, *args, **kwargs):
        """
        Метод для создания экземпляра класса.

        Raises:
            NotImplementedError: Вызывается, если пытаются создать экземпляр абстрактного класса.
        """
        if cls is Organ:
            raise NotImplementedError(f"You cannot create an abstract '{cls.__class__.__name__}' class. Use inheritance")
        return super().__new__(cls)
    
    def get_health(self):
        pass

    def get_max_health(self):
        pass