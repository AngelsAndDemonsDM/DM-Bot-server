import copy
from .prototype_loader import PrototypeLoader


class ReagentPrototypeLoader(PrototypeLoader):
    def __init__(self, file_path, effect_proto_list):
        super().__init__(file_path, "Reagent")
        self._effect_proto_list = effect_proto_list
    
    def _get_func(self, config):
        return self._create_reagent
    
    def _create_reagent(self, config):
        reagent_info = []
        solid_effect = []
        liquid_effect = []
        gas_effect = []

        id = self._validate_config_param(config, "id")

        reagent_info.append(self._validate_config_param(config, "name", id))
        reagent_info.append(self._validate_config_param(config, "desc", id))
        available_states = self._validate_config_param(config, "available_states", id)
        
        for state in available_states:
            if state == "solid":
                solid_effect = self._get_effect_list(config, state, id)
            elif state == "liquid":
                liquid_effect = self._get_effect_list(config, state, id)
            elif state == "gas":
                gas_effect = self._get_effect_list(config, state, id)
            else:
                raise ValueError(f"'{state}' not invluded in the list of avaliable states. reagent:{id}")
        
        reagent_info.append(solid_effect)

        reagent_info.append(liquid_effect)

        reagent_info.append(gas_effect)

        return Reagent(*reagent_info)

    def _get_effect_list(self, config, state: str, id: str):
        state = self._validate_config_param(config, state, id)
        effect_list = []
        
        if state:
            for effect in state:
                effect_id = self._validate_config_param(config, "id", id)
                if effect_id is None:
                    raise ValueError(f"In reagent:{id} effect id is not found.")
                effect = copy.deepcopy(self._effect_proto_list[effect_id])
                tick = self._validate_config_param(config, "tick", id)
                effect.tick = tick
                effect_list.append(effect)
        
        return effect_list
