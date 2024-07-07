from systems.entiti_factory.base_entity import Entity


class PlayerEntity(Entity):
    __slots__ = ['name']

    def __init__(self, entity_id, entity_type, name='Default Player'):
        super().__init__(entity_id, entity_type)
        self.name = name

    def __repr__(self):
        return f"PlayerEntity(id={self.id}, type={self.type}, name={self.name}, components={self.components})"

    @classmethod
    def default_values(cls):
        return {'name': 'Default Player'}

class EnemyEntity(Entity):
    __slots__ = ['strength']

    def __init__(self, entity_id, entity_type, strength=10):
        super().__init__(entity_id, entity_type)
        self.strength = strength

    def __repr__(self):
        return f"EnemyEntity(id={self.id}, type={self.type}, strength={self.strength}, components={self.components})"

    @classmethod
    def default_values(cls):
        return {'strength': 10}
