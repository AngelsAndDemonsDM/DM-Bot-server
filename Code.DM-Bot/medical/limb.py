from etc import Effect

from .base_medical_class import BaseMedicalClass
from .disease import Disease
from .implant import Implant
from .organ import Organ


class Limb(BaseMedicalClass):
    def __init__(self, id: str, name: str, description: str, base_effect: Effect, base_efficiency: float, max_hp: float, cur_hp: float) -> None:
        super().__init__(id, name, description, base_effect, base_efficiency, max_hp, cur_hp)
        self._organs: list[Organ]
        self._diseases: list[Disease]
        self._implants: list[Implant]

    # Get metods
    @property
    def organs(self) -> list[Organ]:
        return self._organs 

    @property
    def diseases(self) -> list[Disease]:
        return self._diseases
    
    @property
    def implants(self) -> list[Implant]:
        return self._implants

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
            self.update_efficiency()
        
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
            self.update_efficiency()
        
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
    # def update_efficiency(self) -> None:
    #     value = 0


    #     # О боже блять | TODO ВЫЧИСЛЕНИЯ ТУТ ПРОСТО КОНСКИЕ БЛЯТЬ. УПРОСТИТЬ
    #     # Создание списка всех эффектов
    #     diseases_effects: list[Effect] = [effect for limb in self._limbs for effect in limb.diseases.effects]
    #     implants_effects: list[Effect] = [effect for limb in self._limbs for effect in limb.implants.effects]
    #     organs_effects: list[Effect]   = [effect for limb in self._limbs for effect in limb.organs.effects]

    #     # Объединение всех эффектов в один список
    #     all_effects = diseases_effects + implants_effects + organs_effects

    #     for effect in all_effects:
    #         if effect.type == "limb_efficiency_mod":
    #             value += effect.strength
        
    #     self._base_effect.strength = (self._base_efficiency * (self._cur_hp/self._max_hp)) + value
    #     # Я хочу плакать