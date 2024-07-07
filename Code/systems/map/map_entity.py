from systems.entity_factory.base_entity import Entity


class MapEntity(Entity):
    __slots__ = ['name']

    def __init__(self, entity_id, entity_type, name='NullSpace'):
        super().__init__(entity_id, entity_type)
        self.name: str = str(name)

    def __repr__(self):
        return f"PlayerEntity(id={self.id}, type={self.type}, name={self.name}, components={self.components})"

    @classmethod
    def default_values(cls):
        return {'name': 'NullSpace'}