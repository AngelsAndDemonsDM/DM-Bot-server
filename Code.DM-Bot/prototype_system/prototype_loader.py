import os
import yaml

class PrototypeLoader:
    def __init__(self, file_path, type: str = None):
        directory_path = os.path.join(os.getcwd(), 'Prototype.DM-Bot', file_path)

        if type is None:
            raise NotImplementedError(f"{self.__class__.__name__} does not have an established prototype type to read")

        self._id_set = set(organ.id for organ in self._prototypes)
        self._prototypes = self._load_prototypes(directory_path, type.lower())

    def _load_prototypes(self, directory_path, type):
        prototypes = []

        for root, dirs, files in os.walk(directory_path):
            for file_name in files:
                if file_name.endswith('.yml'):
                    file_path = os.path.join(root, file_name)
                    with open(file_path, 'r', encoding='utf-8') as file:
                        prototypes_config = yaml.safe_load(file)

                        for config in prototypes_config:
                            if str(config.get('type')).lower() != type:
                                continue

                            subtype = str(config.get('subtype')).lower()
                            creator_func = getattr(self, f"_create_{subtype}", None)

                            if creator_func:
                                organ = creator_func(config, subtype)
                                if organ.id in self._id_set:
                                    raise ValueError(f"Duplicate id '{organ.id}' found.")
                                prototypes.append(organ)
                                self._id_set.add(organ.id)
                            else:
                                raise TypeError(f"Cannot call function {creator_func} in '{self.__class__.__name__}'. Subtype: {subtype}")

        return prototypes
    
    def _validate_config_param(self, config, param_name, id="Unknown prototype"):
        param_value = config.get(param_name)

        if param_value is None:
            raise ValueError(f"Parameter '{param_name}' is missing in the prototype: '{id}'.")
        
        return param_value

    def __getitem__(self, key: str):
        for organ in self._prototypes:
            if organ.id == key:
                return organ
        
        return None

    @property
    def prototypes(self) -> list:
        return self._prototypes
