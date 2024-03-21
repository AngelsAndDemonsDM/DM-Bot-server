class Observer:
    def __init__(self):
        self.subscribers = []

    def attach(self, func):
        self.subscribers.append(func)

    def detach(self, func):
        if func in self.subscribers:
            self.subscribers.remove(func)

    def notify(self, *args, **kwargs):
        for subscriber in self.subscribers:
            subscriber(*args, **kwargs)
