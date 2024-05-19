from base_classes import PrototypeLoader
from effect import Effect


class EffectPrototypeLoader(PrototypeLoader):
    def __init__(self, file_path):
        super().__init__(file_path, "Effect")
    
    def _get_func(self, config):
        return self._create_effect
    
    def _create_effect(self, config):
        cur_id = self._validate_config_param(config, "id")

        return Effect(cur_id, *self._set_params(config, ["name", "desc"], cur_id), 0)
