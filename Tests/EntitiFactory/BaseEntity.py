import unittest

from Code.systems.entiti_factory import Entity


class Component:
    def __init__(self, name):
        self.name = name
        self.owner = None


class TestEntity(Entity):
    def __repr__(self):
        return f"TestEntity(id={self.id}, type={self.type})"


class TestEntityClass(unittest.TestCase):
    def setUp(self):
        self.entity = TestEntity(entity_id=1, entity_type='TestType')
        self.component = Component(name='TestComponent')

    def test_initialization(self):
        self.assertEqual(self.entity.id, 1)
        self.assertEqual(self.entity.type, 'TestType')
        self.assertEqual(self.entity.components, {})

    def test_add_component(self):
        self.entity.add_component('TestComponent', self.component)
        self.assertIn('TestComponent', self.entity.components)
        self.assertEqual(self.entity.components['TestComponent'], self.component)
        self.assertEqual(self.component.owner, self.entity)

    def test_get_component(self):
        self.entity.add_component('TestComponent', self.component)
        component = self.entity.get_component('TestComponent')
        self.assertEqual(component, self.component)
        self.assertIsNone(self.entity.get_component('NonExistentComponent'))

    def test_default_values(self):
        self.assertEqual(TestEntity.default_values(), {})

    def test_repr(self):
        repr_str = repr(self.entity)
        self.assertEqual(repr_str, "TestEntity(id=1, type=TestType)")


if __name__ == '__main__':
    unittest.main()
