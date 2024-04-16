from .disease import Disease
from .organ import Organ
from .implant import Implant
from etc.base_classes.base_object import BaseObject

class Limb(BaseObject):
    def __init__(self, id: str, name: str, description: str) -> None:
        super.__init__(id, name, description)
        self._efficiency_type: str
        self._base_efficiency: float
        self._max_hp: float
        self._organs: list[Organ]
        self._diseases: list[Disease]
        self._implants: list[Implant]

        self._cur_hp: float
        self._cur_efficiency: float

    # Get metods
    @property
    def efficiency_type(self) -> str:
        return self._efficiency_type
    
    @property
    def efficiency(self) -> float:
        return self._cur_efficiency

    @property
    def max_hp(self) -> float:
        return self._max_hp

    @property
    def organs(self) -> list[Organ]:
        return self._organs 

    @property
    def diseases(self) -> list[Disease]:
        return self._diseases
    
    @property
    def implants(self) -> list[Implant]:
        return self._implants

    @property
    def hp(self) -> float:
        return self._cur_hp

    # Set metods
    @efficiency_type.setter
    def efficiency_type(self, value: str) -> None:
        self._efficiency_type = value
    
    @max_hp.setter
    def max_hp(self, value: float) -> None:
        self._max_hp = value

    # Class metods
    # Base add/rm/find
    def _base_add(self, value: object, check_by_id: bool, cur_list: list) -> bool:
        flag: bool = False

        if check_by_id:
            flag = True

            for obj in cur_list:
                if obj.id == value.id:
                    flag = False
                    break
        else:
            if value not in cur_list:
                flag = True

        if flag:
            cur_list.append(value)
        
        return flag

    def _base_rm(self, value: object, check_by_id: bool, cur_list: list) -> bool:
        flag: bool = False
        
        if check_by_id:
            for obj in cur_list:
                if obj.id == value.id:
                    flag = True
                    break
        else:
            if value in cur_list:
                flag = True
        
        if flag:
            cur_list.remove(value)
        
        return flag

    def _base_find(self, key: str, cur_list: list) -> object:
        for obj in cur_list:
            if obj.id == key:
                return obj
        
        return None
            
    # Organ control
    def add_organ(self, value, check_by_id: bool) -> bool:
        return self._base_add(value, check_by_id, self._organs)

    def rm_organ(self, value, check_by_id: bool) -> bool:
        return self._base_rm(value, check_by_id, self._organs)
    
    def find_organ(self, key: str) -> Organ:
        return self._base_find(key, self._organs)
    
    # Disease control
    def add_disease(self, value, check_by_id: bool) -> bool:
        return self._base_add(value, check_by_id, self._diseases)
    
    def rm_disease(self, value, check_by_id: bool) -> bool:
        return self._base_rm(value, check_by_id, self._diseases)

    def find_disease(self, key: str) -> Disease:
        return self._base_find(key, self._diseases)

    # Implant control
    def add_implant(self, value, check_by_id: bool) -> bool:
        return self._base_add(value, check_by_id, self._implants)
    
    def rm_implant(self, value, check_by_id: bool) -> bool:
        return self._base_rm(value, check_by_id, self._implants)

    def find_implant(self, key: str) -> Implant:
        return self._base_find(key, self._implants)

    # ETC
    def update_efficiency(self) -> None:
        value = 0

        for list_check in [self._diseases, self._implants]:
            for obj in list_check:
                for effect in obj.effect:
                    if effect.type == "limb_efficiency_mod":
                        value += effect.strength
        
        self._cur_efficiency = (self._base_efficiency* (self._cur_hp/self._max_hp)) + value
