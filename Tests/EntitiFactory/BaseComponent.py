import unittest

from Code.systems.entity_factory import Component


class ConcreteComponent(Component):
    def __repr__(self):
        return f"ConcreteComponent(owner={self.owner})"


class TestComponentClass(unittest.TestCase):
    def setUp(self):
        self.component = ConcreteComponent()

    def test_initialization(self):
        self.assertIsNone(self.component.owner)

    def test_set_owner(self):
        mock_owner = "Entity1"
        self.component.owner = mock_owner
        self.assertEqual(self.component.owner, mock_owner)

    def test_default_values(self):
        self.assertEqual(ConcreteComponent.default_values(), {})

    def test_repr(self):
        repr_str = repr(self.component)
        self.assertEqual(repr_str, "ConcreteComponent(owner=None)")
        mock_owner = "Entity1"
        self.component.owner = mock_owner
        repr_str_with_owner = repr(self.component)
        self.assertEqual(repr_str_with_owner, f"ConcreteComponent(owner={mock_owner})")


if __name__ == '__main__':
    unittest.main()
