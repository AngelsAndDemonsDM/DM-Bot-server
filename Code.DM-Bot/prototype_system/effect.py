from .prototype_loader import PrototypeLoader
from effect import Effect

class EffectPrototypeLoader(PrototypeLoader):
    def __init__(self, file_path):
        super().__init__(file_path, "Effect")
    
    def _get_func(self, config):
        return self._create_effect
    
    def _create_effect(self, config):
        effect_info = []

        id = self._validate_config_param(config, "id")
        effect_info.append(id)
        effect_info.append(self._validate_config_param(config, "name", id))
        effect_info.append(self._validate_config_param(config, "desc", id))
        effect_info.append(self._validate_config_param(config, "strength", id))

        return Effect(*effect_info)
