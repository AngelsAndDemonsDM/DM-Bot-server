from need import Need

from .prototype_loader import PrototypeLoader

class NeedPrototypeLoader(PrototypeLoader):
    def __init__(self, file_path):
        super().__init__(file_path, "Need"):
            
    
    def _get_func(self, config):
        return self._create_need
        
    def _create_need(self, config):
        need_info[]
        
        id = self._validate_config_param(config, "id")
        need_info.append(id)
        need_info.append(self._validate_config_param(config, "name",id))
        need_info.append(self._validate_config_param(config, "desc",id))
        max_value = self._validate_config_param(config, "max_value", id)
        need_info.append(max_value)
        need_info.append(max_value)
        need_info.append(self._validate_config_param(config, "min_value",id))
        need_info.append(self._validate_config_param(config, "count",id))

    
        return Need(*need_info)