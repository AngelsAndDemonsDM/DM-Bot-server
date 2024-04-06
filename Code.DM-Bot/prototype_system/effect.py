from effect import Effect

from .prototype_loader import PrototypeLoader


class EffectPrototypeLoader(PrototypeLoader):
    def __init__(self, file_path):
        super().__init__(file_path, "Effect")
    
    def _get_func(self, config):
        return self._create_effect
    
    def _create_effect(self, config):
        id = self._validate_config_param(config, "id")
        name = self._validate_config_param(config, "name", id)
        desc = self._validate_config_param(config, "desc", id)

        return Effect(id, name, desc, 0)
