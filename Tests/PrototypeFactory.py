import unittest
from unittest.mock import MagicMock, mock_open, patch

from Code.factory import PrototypeError, PrototypeFactory


class TestPrototypeFactory(unittest.TestCase):
    @patch('prototype_factory.os.path.exists', return_value=True)
    @patch('prototype_factory.open', new_callable=mock_open, read_data="""
components:
  HealthComponent: "Code.factory.base_component.HealthComponent"
  PositionComponent: "Code.factory.base_component.PositionComponent"

entities:
  PlayerEntity: "Code.factory.base_entity.PlayerEntity"
  EnemyEntity: "Code.factory.base_entity.EnemyEntity"
""")
    @patch('prototype_factory.importlib.import_module')
    def setUp(self, mock_import_module, mock_open, mock_exists):
        # Mock the imported classes
        self.MockHealthComponent = MagicMock()
        self.MockPositionComponent = MagicMock()
        self.MockPlayerEntity = MagicMock()
        self.MockEnemyEntity = MagicMock()

        # Configure the return values of the import_module mock
        mock_import_module.side_effect = lambda name: {
            'Code.factory.base_component': MagicMock(
                HealthComponent=self.MockHealthComponent,
                PositionComponent=self.MockPositionComponent
            ),
            'Code.factory.base_entity': MagicMock(
                PlayerEntity=self.MockPlayerEntity,
                EnemyEntity=self.MockEnemyEntity
            )
        }[name]

        self.factory = PrototypeFactory()

    def test_create_component(self):
        component = self.factory._create_component('HealthComponent', health=100)
        self.MockHealthComponent.assert_called_with(health=100)
        self.assertEqual(component, self.MockHealthComponent())

    def test_create_entity(self):
        entity_data = {
            'type': 'PlayerEntity',
            'id': 'player1',
            'name': 'Hero',
            'components': [
                {'type': 'HealthComponent', 'health': 100}
            ]
        }
        self.MockPlayerEntity.default_values.return_value = {'name': 'Default Player'}
        self.MockHealthComponent.default_values.return_value = {'health': 100}
        
        entity = self.factory._create_entity(entity_data, 'dummy_path.yml', 1)
        
        self.MockPlayerEntity.assert_called_with(
            entity_id='player1',
            entity_type='PlayerEntity',
            name='Hero'
        )
        self.MockHealthComponent.assert_called_with(health=100)
        self.MockPlayerEntity().add_component.assert_called_with('HealthComponent', self.MockHealthComponent())
        self.assertEqual(entity, self.MockPlayerEntity())

    def test_find_entity(self):
        entity_data = {
            'type': 'PlayerEntity',
            'id': 'player1'
        }
        self.MockPlayerEntity.default_values.return_value = {'name': 'Default Player'}
        
        entity = self.factory._create_entity(entity_data, 'dummy_path.yml', 1)
        found_entity = self.factory.find_entity('PlayerEntity', 'player1')
        
        self.assertEqual(entity, found_entity)
    
    @patch('prototype_factory.glob', return_value=['dummy_path.yml'])
    @patch('prototype_factory.open', new_callable=mock_open, read_data="""
- type: PlayerEntity
  id: player1
  name: Hero
  components:
    - type: HealthComponent
      health: 100
""")
    def test_load_all_entities(self, mock_open, mock_glob):
        self.MockPlayerEntity.default_values.return_value = {'name': 'Default Player'}
        self.MockHealthComponent.default_values.return_value = {'health': 100}
        
        entities = self.factory.load_all_entities()
        
        self.MockPlayerEntity.assert_called_with(
            entity_id='player1',
            entity_type='PlayerEntity',
            name='Hero'
        )
        self.MockHealthComponent.assert_called_with(health=100)
        self.MockPlayerEntity().add_component.assert_called_with('HealthComponent', self.MockHealthComponent())
        
        self.assertEqual(len(entities), 1)
        self.assertEqual(entities[0], self.MockPlayerEntity())

if __name__ == '__main__':
    unittest.main()
