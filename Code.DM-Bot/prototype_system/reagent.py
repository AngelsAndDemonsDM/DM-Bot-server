from reagent.reagent import Reagent

from .prototype_loader import PrototypeLoader


class ReagentPrototypeLoader(PrototypeLoader):
    def __init__(self, file_path, effect_proto_list):
        super().__init__(file_path, "Reagent")
        self._effect_proto_list = effect_proto_list
    
    def _get_func(self, config):
        return self._create_reagent
    
    def _create_reagent(self, config):
        id = self._validate_config_param(config, "id")
        name = self._validate_config_param(config, "name", id)
        desc = self._validate_config_param(config, "desc", id)
        boiling_temp = self._validate_config_param(config, "boiling_temp", id)
        crystal_temp = self._validate_config_param(config, "crystal_temp", id)

        return Reagent(id, name, desc, boiling_temp, crystal_temp, 0)
