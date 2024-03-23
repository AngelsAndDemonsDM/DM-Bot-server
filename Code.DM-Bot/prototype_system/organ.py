import os

import yaml
from medical.medical_enums import BreastSizeEnum, GenderEnum
from medical.organs.brain import Brain
from medical.organs.breast import Breast
from medical.organs.genitalia import Genitalia
from medical.organs.heart import Heart
from medical.organs.kidney import Kidney
from medical.organs.liver import Liver
from medical.organs.lung import Lung
from medical.organs.stomach import Stomach


class OrganPrototypeLoader:
    def __init__(self, file_path):
        directory_path = os.path.join(os.getcwd(), 'Prototype.DM-Bot', file_path)
        self._prototypes = self._load_prototypes(directory_path)

    def _load_prototypes(self, directory_path):
        prototypes = []

        for root, dirs, files in os.walk(directory_path):
            for file_name in files:
                if file_name.endswith('.yml'):
                    file_path = os.path.join(root, file_name)
                    with open(file_path, 'r', encoding='utf-8') as file:
                        prototypes_config = yaml.safe_load(file)

                        for config in prototypes_config:
                            if str(config.get('type')).lower() != 'organ':
                                continue

                            subtype = str(config.get('subtype')).lower()
                            creator_func = getattr(self, f"_create_{subtype}", None)

                            if creator_func:
                                prototypes.append(creator_func(config, subtype))
                            else:
                                raise TypeError(f"Cannot call function {creator_func} in {self.__class__.__name__}. Subtype: {subtype}")

        return prototypes

    def _create_organ(func):
        def wrapper(self, config, subtype):
            organ_info = []
            organ_info.append(str(config.get("id")))
            organ_info.append(str(config.get("name")))
            organ_info.append(str(config.get("desc")))
            organ_info.append(config.get("max_health"))
            organ_info.append(config.get("standart_efficiency"))
            organ_info.append(subtype)
            return func(self, config, organ_info)
        
        return wrapper

    @_create_organ
    def _create_brain(self, config, organ_info):
        return Brain(*organ_info)

    @_create_organ
    def _create_heart(self, config, organ_info):
        return Heart(*organ_info)
    
    @_create_organ
    def _create_liver(self, config, organ_info):
        return Liver(*organ_info)
    
    @_create_organ
    def _create_kidney(self, config, organ_info):
        return Kidney(*organ_info)
    
    @_create_organ
    def _create_lung(self, config, organ_info):
        return Lung(*organ_info)
    
    @_create_organ
    def _create_stomach(self, config, organ_info):
        organ_info.append(config.get('volume'))

        return Stomach(*organ_info)

    @_create_organ
    def _create_genitalia(self, config, organ_info):
        organ_info.append(GenderEnum[str(config.get("gender_type")).upper()])

        return Genitalia(*organ_info)

    @_create_organ
    def _create_breast(self, config, organ_info):
        organ_info.append(BreastSizeEnum[str(config.get("size")).upper()])

        return Breast(*organ_info)

    def get_prototype(self):
        return self._prototypes
