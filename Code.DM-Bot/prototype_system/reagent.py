from .prototype_loader import PrototypeLoader


class ReagentPrototypeLoader(PrototypeLoader):
    def __init__(self, file_path, effect_list):
        super().__init__(file_path, "Reagent")
    
    def _get_func(self, config):
        return self._create_reagent
    
    def _create_reagent(self, config):
        reagent_info = []

        id = self._validate_config_param(config, "id")

        reagent_info.append(self._validate_config_param(config, "name", id))
        reagent_info.append(self._validate_config_param(config, "desc", id))
        available_states = self._validate_config_param(config, "available_states", id)

        for state in available_states:
            if state not in ["solid", "liquid", "gas"]:
                pass # Похуй, потом. Мозг вмер