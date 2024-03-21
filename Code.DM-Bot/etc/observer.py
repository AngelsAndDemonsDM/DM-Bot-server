class Observer:
    def __init__(self):
        """
        Инициализация нового экземпляра класса Observer.
        """
        self.subscribers = []

    def attach(self, func, num_notifications=float('inf')):
        """
        Подписывает функцию на события.

        Args:
            func (callable): Функция-подписчик.
            num_notifications (float): Количество уведомлений, которые должен получить подписчик (по умолчанию бесконечное количество).
        """
        self.subscribers.append({'func': func, 'num_notifications': num_notifications, 'notifications_received': 0})

    def detach(self, func):
        """
        Отписывает функцию от событий.

        Args:
            func (callable): Функция-подписчик.
        """
        for subscriber in self.subscribers:
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
            subscriber['notifications_received'] += 1
            if subscriber['notifications_received'] >= subscriber['num_notifications']:
                self.detach(subscriber['func'])
