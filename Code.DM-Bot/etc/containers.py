class Item:
	def __init__(self, size: int, item_obj):
        self._size = size              # Определяем размер предмета в числовом выражении, что ранее занесено   
        self._item_obj = item_obj        # Определяем к чему принадлежит предмет
        
    #Get методы
    @property
    def size(self) -> int:
    
        return self._size
        
    @property    
    def item_obj(self):
        
        return self._item_obj
        
    #Set методы
    @size.setter 
    def size(self, size: int):
        self._size = size
        
    @item_obj.setter
    def item_obj(self, item_obj):
        self._item_obj = item_obj
        
    

    # Данные о предмете
    @property
    def item_desc(self):
        try:
            return self._item_obj.description
        except Exception as err:
            return None
    
    @property
    def item_name(self):
        try:
            return self._item_obj.name
        except Exception as err:
            return None
        
    @property    
    def item_id(self):
        try:
            return self._item_obj.id
        except Exception as err:
            return None
            