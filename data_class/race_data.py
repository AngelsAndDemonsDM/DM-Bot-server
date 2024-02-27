# TODO:
# Таланты расы
# Влияние на статы
# Особенности расы
# Нужды расы

class Talant:
    def __init__(self, id = None, name = None, desc = None, tags = {}):     # Default значения
        if id is None: 
            self.id = id
        elif not self.set_id(id):
            raise TypeError("ID in Talatn must be 'String' type.")
            
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

