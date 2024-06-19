import importlib
import os
import unittest
from unittest.mock import MagicMock, mock_open, patch

from Code.factory import PrototypeError, PrototypeFactory


class TestPrototypeFactory(unittest.TestCase):
    def setUp(self):
        # Mock os.path.exists to always return True
        patcher_exists = patch('os.path.exists', return_value=True)
        self.mock_exists = patcher_exists.start()
        self.addCleanup(patcher_exists.stop)

        # Mock open to provide dummy class mappings
        self.dummy_class_mappings = """
components:
  HealthComponent: "Code.factory.base_component.HealthComponent"
  PositionComponent: "Code.factory.base_component.PositionComponent"

entities:
  PlayerEntity: "Code.factory.base_entity.PlayerEntity"
  EnemyEntity: "Code.factory.base_entity.EnemyEntity"
"""
        patcher_open = patch('builtins.open', mock_open(read_data=self.dummy_class_mappings))
        self.mock_open = patcher_open.start()
        self.addCleanup(patcher_open.stop)

        # Mock importlib.import_module to return mock classes
        self.MockHealthComponent = MagicMock()
        self.MockPositionComponent = MagicMock()
        self.MockPlayerEntity = MagicMock()
        self.MockEnemyEntity = MagicMock()

        def import_module_mock(name):
            if name == 'Code.factory.base_component':
                return MagicMock(
                    HealthComponent=self.MockHealthComponent,
                    PositionComponent=self.MockPositionComponent
                )
            elif name == 'Code.factory.base_entity':
                return MagicMock(
                    PlayerEntity=self.MockPlayerEntity,
                    EnemyEntity=self.MockEnemyEntity
                )
            raise ImportError(f"No module named '{name}'")

        patcher_import = patch('importlib.import_module', side_effect=import_module_mock)
        self.mock_import_module = patcher_import.start()
        self.addCleanup(patcher_import.stop)

        # Create the factory instance
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
    
    def test_load_all_entities(self):
        # Mock glob to return a dummy file list
        patcher_glob = patch('glob.glob', return_value=['dummy_path.yml'])
        mock_glob = patcher_glob.start()
        self.addCleanup(patcher_glob.stop)

        # Mock open to provide dummy entity data
        dummy_entity_data = """
- type: PlayerEntity
  id: player1
  name: Hero
  components:
    - type: HealthComponent
      health: 100
"""
        patcher_open = patch('builtins.open', mock_open(read_data=dummy_entity_data))
        mock_open = patcher_open.start()
        self.addCleanup(patcher_open.stop)

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
