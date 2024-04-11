from .organ import Organ
from .disease import Disease

class Limb:
    def __init__(self) -> None:
        self._id: str
        self._name: str 
        self._description: str
        self._efficiency_type: str
        self._base_efficiency: float
        self._max_hp: float
        self._organs: list[Organ]
        self._diseases: list[Disease]

        self._cur_hp: float

    # get metods
    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name
    
    @property
    def description(self) -> str:
        return self._description
    
    @property
    def efficiency_type(self) -> str:
        return self._efficiency_type
    
    @property
    def max_hp(self) -> float:
        return self._max_hp

    def organ_find(self, key: str) -> Organ:
        for organ in self._organs:
            if organ.id == key:
                return organ
        
        return None

    @property
    def organs(self) -> list[Organ]:
        return self._organs 
    
    def diseases_find(self, key: str) -> Disease:
        for disease in self._diseases:
            if disease.id == key:
                return disease
        
        return None

    @property
    def diseases(self) -> list[Disease]:
        return self._diseases
    
    @property
    def hp(self) -> float:
        return self._cur_hp

    # set metods
    @id.setter
    def id (self, value: str) -> None:
        self._id = value

    @name.setter
    def name(self, value: str) -> None:
        self._name = value
    
    @description.setter
    def description(self, value: str) -> None:
        self._description = value

    @efficiency_type.setter
    def efficiency_type(self, value: str) -> None:
        self._efficiency_type = value
    
    @max_hp.setter
    def max_hp(self, value: float) -> None:
        self._max_hp = value

    # class metods
    def add_organ(self, value: Organ, check_by_id: bool) -> bool:
        match check_by_id:
            case True:
                flag: bool = True
                for organ in self._organs:
                    if organ.id == value.id:
                        flag = False
                        break
                
                if flag:
                    self._organs.append(value)
                    return True
                else:
                    return False
            
            case False:
                if value not in self._organs:
                    self._organs.append(value)
                    return True
                
                return False
    
    def rm_organ(self, value: Organ, check_by_id: bool) -> bool:
        match check_by_id:
            case True:
                for organ in self._organs:
                    if organ.id == value.id:
                        self._organs.remove(organ)
                        return True                
                
                return False
            
            case False:
                if value in self._organs:
                    self._organs.remove(value)
                    return True
                
                return False

    def add_disease(self, value: Disease, check_by_id: bool) -> bool:
        match check_by_id:
            case True:
                flag: bool = True
                for disease in self._diseases:
                    if disease.id == value.id:
                        flag = False
                        break
                
                if flag:
                    self._diseases.append(value)
                    return True
                else:
                    return False
            
            case False:
                if value not in self._diseases:
                    self._diseases.append(value)
                    return True
                
                return False
    
    def rm_disease(self, value: Disease, check_by_id: bool) -> bool:
        match check_by_id:
            case True:
                for disease in self._diseases:
                    if disease.id == value.id:
                        self._diseases.remove(disease)
                        return True
                
                return False
            
            case False:
                if value in self._diseases:
                    self._diseases.remove(value)
                    return True
                
                return False
