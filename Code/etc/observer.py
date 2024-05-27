class Observer:
    def __init__(self):
        """
        Инициализация нового экземпляра класса Observer.
        """
        self.subscribers = []

    def attach(self, func, remaining=-1):
        """
        Подписывает функцию на события.

        Args:
            func (callable): Функция-подписчик.
            remaining (int): Количество уведомлений, которые должен получить подписчик (по умолчанию бесконечное количество).
        """
        self.subscribers.append({'func': func, 'remaining': remaining})

    def detach(self, func):
        """
        Отписывает функцию от событий.

        Args:
            func (callable): Функция-подписчик.
        """
        for subscriber in self.subscribers[:]:  
            if subscriber['func'] == func:
                self.subscribers.remove(subscriber)

    def notify(self, *args, **kwargs):
        """
        Оповещает всех подписчиков о событии.

        Args:
            args: Позиционные аргументы для передачи подписчикам.
            kwargs: Именованные аргументы для передачи подписчикам.
        """
        for subscriber in self.subscribers[:]:  
            subscriber['func'](*args, **kwargs)
            if subscriber['remaining'] != -1:
                subscriber['remaining'] -= 1
                if subscriber['remaining'] == 0:
                    self.detach(subscriber['func'])
