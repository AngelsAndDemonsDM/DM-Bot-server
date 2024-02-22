import json
import os


class PlayerManager:
    def __init__(self):
        self.path = os.path.join(os.getcwd(), '..', 'data', 'players', 'player_data.json')
    
    def save_file(self):
        """
        Сохранение данных о игроке
        
        Args:
            None
        
        Returns:
            None
        """
        with open(self.path, 'w') as file:
            json.dump(self.data, file, indent=4)
    
    
    def load_file(self):
        """
        Получение расы игрока
        
        Args:
            None
        
        Returns:
            data (DataFiles): Загруженный файл данных
        """
        with open(self.path, 'r') as file:
            return json.load(file)
    