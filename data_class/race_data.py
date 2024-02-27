# TODO:
# Влияние на статы
# Особенности расы
# Нужды расы

# Таланты расы
class Talant:
    def __init__(self, id = None, name = None, desc = None, tags = {}):     # Default значения
        if id is None: 
            self.id = id
        elif not self.set_id(id):
            raise TypeError("ID in Talant must be 'String' type.")
            
        if name is None:
            self.name = name
        elif not self.set_name(name):
            raise TypeError("Name in Talant must be 'String' type.")
        
        self.desc 
        if desc is None:
            self.desc = desc
        elif not self.set_desc(desc):
            raise TypeError("Desc in Talant must be 'String' type.")
            
        self.tags 
        if not self.set_tags(tags):
            raise TypeError("Tags in Talant must be 'List' type.")
    
    # Get методы
    def get_id(self):
        return self.id
    
    def get_name(self):
        return self.name
    
    def get_decs(self):
        return self.decs
        
    def get_tags(self):
        return self.tags
     
    # Set методы
    def set_id(self, id):
        if isinstance(id, (str, int, float)):
            self.id = id
            return True
            
        return False
    
    def set_name(self, name):
        if isinstance(self, (str, int, float)):
            self.name = name
            return True
        
        return False
        
    def set_desc(self, desc):
        if isinstance(desc, (str, int, float)):
            self.desc = desc
            return True
        
        return False
        
    def set_tags(self, tags):
        if isinstance(tags, list):
            self.tags = tags
            return True
        
        return False

# Нужды расы
class Needs:
    def __init__(self, id = None, name = None, desc = None, value = 0, max = 100, min = -100, count = -1):
        self.id
        if id is None:                   # ID потребности
            self.id = id
        elif not self.set_id(id):
            raise TypeError("ID in Needs must be 'String' type.")
        
        self.name
        if name is None:                 # Наименование
            self.name = name
        elif not self.set_name(name):
            raise TypeError("Name in Needs must be 'String' type")
        
        self.desc
        if desc is None:                 # Описание
            self.desc = desc
        elif not self.set_desc(desc):
            raise TypeError("Desc in Needs must be 'String' type")
            
        
        self.value
        elif not self.set_value(value):  # Текущее значение
            raise TypeError("Value in Needs must be 'Interiger' type")
            
        self.max    
        elif not self.set_max(max):       # Максимальное значение
            raise TypeError("Max in Needs must be 'Interiger' type")
            
        self.min    
        elif not self.set_min(min):       # Минимальное значение
            raise TypeError("Min in Needs must be 'Interiger' type")
        
        self.count
        elif not self.set_count(count):   # Дельта изменения за ход/тик
            raise TypeError("Count in Needs must be 'Interiger' type")
    
    # Get методы
    def get_id(self):
        return self.id
        
    def get_name(self):
        return self.name
        
    def get_desc(self):
        return self.desc
        
    def get_value(self):
        return self.value
        
    def get_max(self):
        return self.max
        
    def get_min(self):
        return self.min
      
    def get_count(self):
        return self.count
    
    # Set методы
    def set_id(self, id):
        if isinstance(id, (str, int, float)):
            self.id = id
            return True
        
        return False
        
    def set_name(self, name):
        if isinstance(name, (str, int, float)):
            self.name = name
            return True
            
        return False
        
    def set_desc(self, decs):
        if isinstance(decs, (str, int, float)):
            self.desc = desc
            return True
        
        return False
        
    def set_value(self, value):
        if isinstance(value, (int, float)):
            if value>self.max:
                self.value = self.max
            elif value<self.min:
                self.value = self.min 
            self.value = int(value)
            return True
            
        return False 
        
    def set_max(self, max):
        if isinstance(max, (int, float)):
            self.max = int(max)
            return True
        
        return False
        
    def set_min(self, min):
        if isinstance(min, (int, float)):
            self.min = int(min) 
            return True
            
        return False
        
    def set_count(self, count):
        if isinstance(count, (int, float)):
            self.count = int(count)
            return True
            
        return False
        
    def uptake(self): # Изменение в ход/тик 
        ut = self.value
        ut += self.count
        self.set_value(ut)
        
    def value_change(self, number): # Изменение на нужное число
        if isinstance(number, (int, float)):
            number = int(number)
            vc = self.value
            vc += number
            self.set_value(vc)
        else:
            raise TypeError("Number in value_change must be 'Interiger' or 'Float' type")
            