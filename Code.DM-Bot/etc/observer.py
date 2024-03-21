class Observer:
        def __init__(self):
                """
                        Инициализирует новый экземпляр класса Observer.
                                """
                                        self.subscribers = []

                                            def attach(self, func, num_notifications=float('inf')):
                                                    """
                                                            Подписывает функцию на события.

                                                                    :param func: Функция-подписчик.
                                                                            :param num_notifications: Количество уведомлений, которые должен получить подписчик (по умолчанию бесконечное количество).
                                                                                    """
                                                                                            self.subscribers.append({'func': func, 'num_notifications': num_notifications, 'notifications_received': 0})

                                                                                                def detach(self, func):
                                                                                                        """
                                                                                                                Отписывает функцию от событий.

                                                                                                                        :param func: Функция-подписчик.
                                                                                                                                """
                                                                                                                                        for subscriber in self.subscribers:
                                                                                                                                                    if subscriber['func'] == func:
                                                                                                                                                                    self.subscribers.remove(subscriber)

                                                                                                                                                                        def notify(self, *args, **kwargs):
                                                                                                                                                                                """
                                                                                                                                                                                        Оповещает всех подписчиков о событии.

                                                                                                                                                                                                :param args: Позиционные аргументы для передачи подписчикам.
                                                                                                                                                                                                        :param kwargs: Именованные аргументы для передачи подписчикам.
                                                                                                                                                                                                                """
                                                                                                                                                                                                                        for subscriber in self.subscribers[:]:  # Создаем копию списка, чтобы избежать проблем с удалением элементов во время итерации
                                                                                                                                                                                                                                    subscriber['func'](*args, **kwargs)
                                                                                                                                                                                                                                                subscriber['notifications_received'] += 1
                                                                                                                                                                                                                                                            if subscriber['notifications_received'] >= subscriber['num_notifications']:  # Если подписчик получил все уведомления, отписываем его
                                                                                                                                                                                                                                                                            self.detach(subscriber['func'])