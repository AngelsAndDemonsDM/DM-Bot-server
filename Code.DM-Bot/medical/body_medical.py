from etc import Effect

from .disease import Disease
from .implant import Implant
from .limb import Limb
from .organ import Organ


class BodyMedical:
    def __init__(self) -> None:
        # Stats
        self._body_stats: dict = { # Инициализируем всё по 0.0. Мне похуй.
            "cognitive": 0.0,    # сознание
            "pain": 0.0,         # боль
            "vision": 0.0,       # зрение
            "hearing": 0.0,      # слух
            "scent": 0.0,        # обоняние
            "productivity": 0.0, # работа
            "movement": 0.0,     # передвижение
            "fertility": 0.0,    # фертильность
        }

        # Needs
        # TODO

        # Limbs
        self._limbs: list[Limb]
        # TODO

    def get_stat(self, key: str):
        """
        Возвращает значение статистики по ключу.

        Значение ключей:
        cognitive:    сознание
        pain:         боль
        vision:       зрение
        hearing:      слух
        scent:        обоняние
        productivity: работа
        movement:     передвижение
        fertility:    фертильность

        Args:
            key (str): Ключ статистики.

        Returns:
            value(Any or None): Возвращает или значение статистики или None если не нашёл ключ.
        """
        return self._body_stats.get(key, None)

    # Идея на заметку - сделать отдельный лист с этим всем говном для ускорения
    def update_stats(self) -> None:

        self._body_stats: dict = { # Сносим значения до 0. Потом считаем
            "cognitive": 0.0,    # сознание
            "pain": 0.0,         # боль
            "vision": 0.0,       # зрение
            "hearing": 0.0,      # слух
            "scent": 0.0,        # обоняние
            "productivity": 0.0, # работа
            "movement": 0.0,     # передвижение
            "fertility": 0.0,    # фертильность
        }

        # Получаем все списки.
        # Лимбы уже есть
        diseases_list: list[Disease] = [disease for limb in self._limbs for disease in limb.diseases] # Все болезни
        implants_list: list[Implant] = [implant for limb in self._limbs for implant in limb.implants] # Все импланты
        organs_list: list[Organ]     = [organ for limb in self._limbs for organ in limb.organs]       # Все органы

        # Считаем весь пиздец
        for limb in self._limbs:
            self._apply_body_effect(limb.base_effect)
        
        for implant in implants_list:
            self._apply_body_effect(implant.base_effect)
            for effect in implant.effects:
                self._apply_body_effect(effect)

        for disease in diseases_list:
            for effect in disease.effects:
                self._apply_body_effect(effect)
        
        for organ in organs_list:
            self._apply_body_effect(organ.base_effect)
            for effect in organ.effects:
                self._apply_body_effect(effect)


    def _apply_body_effect(self, effect: Effect) -> None:
        if effect.type.startswith("body_") and effect.type.endswith("_mod"):
                stat_name = effect.type.split("_")[1]
                        
                if stat_name in self._body_stats:
                    self._body_stats[stat_name] += effect.strength