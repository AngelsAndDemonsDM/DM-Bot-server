from base_classes import PrototypeLoader
from need import Need


class NeedPrototypeLoader(PrototypeLoader):
    def __init__(self, file_path):
        super().__init__(file_path, "Need")
    
    def _get_func(self, config):
        return self._create_need
        
    def _create_need(self, config):
            id = self._validate_config_param(config, "id")
            name = self._validate_config_param(config, "name", id)
            desc = self._validate_config_param(config, "desc", id)
            max_value = self._validate_config_param(config, "max_value", id)
            min_value = self._validate_config_param(config, "min_value", id)
            count = self._validate_config_param(config, "count", id)

            return Need(id, name, desc, max_value, min_value, count)
