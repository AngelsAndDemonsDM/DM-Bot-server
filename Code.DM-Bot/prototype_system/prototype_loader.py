import os
import yaml

class PrototypeLoader:
    def __new__(cls, *args, **kwargs):
        """
        Метод для создания экземпляра класса.

        Raises:
            NotImplementedError: Вызывается, если пытаются создать экземпляр абстрактного класса PrototypeLoader.
        """
        if cls is PrototypeLoader:
            raise NotImplementedError("You cannot create an abstract 'PrototypeLoader' class. Use inheritance")
        return super().__new__(cls)

    def __init__(self, file_path, type: str = None):
        directory_path = os.path.join(os.getcwd(), 'Prototype.DM-Bot', file_path)

        if type is None:
            raise NotImplementedError(f"{self.__class__.__name__} does not have an established prototype type to read")
        self._type = type.lower()
        self._id_set = set()
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
                            if str(config.get('type')).lower() != self._type:
                                continue

                            creator_func = self._get_func(config)

                            if creator_func:
                                proto = creator_func(config)
                                if proto.id in self._id_set:
                                    raise ValueError(f"Duplicate id '{proto.id}' found.")
                                prototypes.append(proto)
                                self._id_set.add(proto.id)
                            else:
                                raise TypeError(f"Cannot call function {creator_func} in '{self.__class__.__name__}'")

        return prototypes
    
    def _get_func(self, config):
        raise NotImplementedError(f"The method '_get_func' in class '{self.__class__.__name__}' must be overridden.")

    def _validate_config_param(self, config, param_name, id="Unknown prototype"):
        param_value = config.get(param_name)

        if param_value is None:
            raise ValueError(f"Parameter '{param_name}' is missing in the prototype: '{id}'.")
        
        return param_value

    def __getitem__(self, key: str):
        for prototype in self._prototypes:
            if prototype.id == key:
                return prototype
        
        return None

    @property
    def prototypes(self) -> list:
        return self._prototypes
