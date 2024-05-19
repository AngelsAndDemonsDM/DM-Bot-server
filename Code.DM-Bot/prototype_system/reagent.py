from base_classes import PrototypeLoader
from reagent.reagent import Reagent


class ReagentPrototypeLoader(PrototypeLoader):
    def __init__(self, file_path, effect_proto_list):
        super().__init__(file_path, "Reagent")
        self._effect_proto_list = effect_proto_list
    
    def _get_func(self, config):
        return self._create_reagent
    
    def _create_reagent(self, config):
        cur_id = self._validate_config_param(config, "id")

        return Reagent(cur_id, *self._set_params(config, ["name", "desc", "boiling_temp", "crystal_temp"], cur_id), 0)
