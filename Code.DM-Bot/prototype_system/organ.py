from .prototype_loader import PrototypeLoader
from medical.medical_enums import BreastSizeEnum, GenderEnum
from medical.organs.brain import Brain
from medical.organs.breast import Breast
from medical.organs.genitalia import Genitalia
from medical.organs.heart import Heart
from medical.organs.kidney import Kidney
from medical.organs.liver import Liver
from medical.organs.lung import Lung
from medical.organs.stomach import Stomach


class OrganPrototypeLoader(PrototypeLoader):
    def __init__(self, file_path):
        super().__init__(file_path, "Organ")

    def _create_organ(func):
        def wrapper(self, config):
            organ_info = []
            id = self._validate_config_param(config, "id")
            organ_info.append(id)
            organ_info.append(self._validate_config_param(config, "name", id))
            organ_info.append(self._validate_config_param(config, "desc", id))
            organ_info.append(self._validate_config_param(config, "max_health", id))
            organ_info.append(self._validate_config_param(config, "standart_efficiency", id))
            organ_info.append(self._validate_config_oaram(config, "subtype", id))
            return func(self, config, organ_info, id)
        
        return wrapper

    def _get_func(self, config):
        subtype = str(config.get('subtype')).lower()
        return getattr(self, f"_create_{subtype}", None)

    @_create_organ
    def _create_brain(self, config, organ_info, id):
        return Brain(*organ_info)

    @_create_organ
    def _create_heart(self, config, organ_info, id):
        return Heart(*organ_info)
    
    @_create_organ
    def _create_liver(self, config, organ_info, id):
        return Liver(*organ_info)
    
    @_create_organ
    def _create_kidney(self, config, organ_info, id):
        return Kidney(*organ_info)
    
    @_create_organ
    def _create_lung(self, config, organ_info, id):
        return Lung(*organ_info)
    
    @_create_organ
    def _create_stomach(self, config, organ_info, id):
        organ_info.append(self._validate_config_param(config, 'volume', id))
        return Stomach(*organ_info)

    @_create_organ
    def _create_genitalia(self, config, organ_info, id):
        organ_info.append(GenderEnum[str(self._validate_config_param(config, "gender_type", id)).upper()])
        return Genitalia(*organ_info)

    @_create_organ
    def _create_breast(self, config, organ_info, id):
        organ_info.append(BreastSizeEnum[str(self._validate_config_param(config, "size", id)).upper()])
        organ_info.append(self._validate_config_param(config, 'reagent_per_day', id))    
        organ_info.append(self._validate_config_param(config, 'reagent_per_tick', id))  
        organ_info.append(self._validate_config_param(config, 'amount_reagent', id))
        return Breast(*organ_info)
