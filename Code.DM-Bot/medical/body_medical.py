from etc import Effect

from .limb import Limb


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

        # О боже блять | TODO ВЫЧИСЛЕНИЯ ТУТ ПРОСТО КОНСКИЕ БЛЯТЬ. УПРОСТИТЬ
        # Создание списка всех эффектов
        diseases_effects: list[Effect] = [effect for limb in self._limbs for effect in limb.diseases.effects]
        implants_effects: list[Effect] = [effect for limb in self._limbs for effect in limb.implants.effects]
        organs_effects: list[Effect]   = [effect for limb in self._limbs for effect in limb.organs.effects]

        # Объединение всех эффектов в один список
        all_effects = diseases_effects + implants_effects + organs_effects

        for effect in all_effects:
            if effect.type.startswith("body_") and effect.type.endswith("_mod"):
                stat_name = effect.type.split("_")[1]
                        
                if stat_name in self._body_stats:
                    self._body_stats[stat_name] += effect.strength
        # brain dead
