from base_classes import PrototypeLoader
from need import Need


class NeedPrototypeLoader(PrototypeLoader):
    def __init__(self, file_path):
        super().__init__(file_path, "Need")
    
    def _get_func(self, config):
        return self._create_need
        
    def _create_need(self, config):
        cur_id = self._validate_config_param(config, "id")

        return Need(cur_id, *self._set_params(config, ["name", "desc", "max_value", "min_value", "count"], cur_id))
