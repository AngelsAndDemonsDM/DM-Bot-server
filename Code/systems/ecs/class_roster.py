ENTITY_REGISTRY = {}
COMPONENT_REGISTRY = {}


# Декораторы для регистрации классов в реестрах
def register_entity(cls):
    ENTITY_REGISTRY[cls.__name__] = cls
    return cls


def register_component(cls):
    COMPONENT_REGISTRY[cls.__name__] = cls
    return cls
