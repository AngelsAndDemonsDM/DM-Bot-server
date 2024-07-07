import os
import shutil
import tempfile
import unittest

from Code.systems.entity_factory import PrototypeFactory

HEALTH_COMPONENT_PATH: str = "systems.entity_factory.test_fold.component.HealthComponent"
POSITION_COMPONENT_PATH: str = "Code.systems.entity_factory.test_fold.component.PositionComponent"
PLAYER_ENTITY_PATH: str = "Code.systems.entity_factory.test_fold.entity.PlayerEntity"
ENEMY_ENTITY_PATH: str = "systems.entity_factory.test_fold.entity.EnemyEntity"

class TestPrototypeFactory(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

        self.factory_mappings = f"""
components:
  HealthComponent: "{HEALTH_COMPONENT_PATH}"
  PositionComponent: "{POSITION_COMPONENT_PATH}"

entities:
  PlayerEntity: "{PLAYER_ENTITY_PATH}"
  EnemyEntity: "{ENEMY_ENTITY_PATH}"
"""
        self.factory_mappings_path = os.path.join(self.test_dir, 'factory_mappings.yml')
        with open(self.factory_mappings_path, 'w', encoding='utf-8') as f:
            f.write(self.factory_mappings)

        self.entity_data = """
- type: PlayerEntity
  id: player1
  name: Hero
  components:
    - type: HealthComponent
      health: 100
"""
        self.entity_file_path = os.path.join(self.test_dir, 'entity.yml')
        with open(self.entity_file_path, 'w', encoding='utf-8') as f:
            f.write(self.entity_data)

        self.factory = PrototypeFactory(prototype_dir=self.test_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_create_component(self):
        component_class = self.factory._load_class(HEALTH_COMPONENT_PATH)
        component = component_class(health=100)
        self.assertEqual(component.health, 100)

    def test_create_entity(self):
        entity_data = {
            'type': 'PlayerEntity',
            'id': 'player1',
            'name': 'Hero',
            'components': [
                {'type': 'HealthComponent', 'health': 100}
            ]
        }

        entity_class = self.factory._load_class(PLAYER_ENTITY_PATH)
        entity_class.default_values = lambda: {'name': 'Default Player'}
        component_class = self.factory._load_class(HEALTH_COMPONENT_PATH)
        component_class.default_values = lambda: {'health': 100}
        
        entity = self.factory._create_entity(entity_data, 'dummy_path.yml', 1)
        
        self.assertEqual(entity.id, 'player1')
        self.assertEqual(entity.type, 'PlayerEntity')
        self.assertEqual(entity.name, 'Hero')
        self.assertEqual(entity.components['HealthComponent'].health, 100)

    def test_find_entity(self):
        entity_data = {
            'type': 'PlayerEntity',
            'id': 'player1'
        }

        entity_class = self.factory._load_class(PLAYER_ENTITY_PATH)
        entity_class.default_values = lambda: {'name': 'Default Player'}
        
        entity = self.factory._create_entity(entity_data, 'dummy_path.yml', 1)
        found_entity = self.factory.find_entity('PlayerEntity', 'player1')
        
        self.assertIsNotNone(found_entity)
        self.assertEqual(found_entity.id, 'player1')

    def test_load_all_entities(self):
        entity_class = self.factory._load_class(PLAYER_ENTITY_PATH)
        entity_class.default_values = lambda: {'name': 'Default Player'}
        component_class = self.factory._load_class(HEALTH_COMPONENT_PATH)
        component_class.default_values = lambda: {'health': 100}
        
        entities = self.factory.load_all_entities()
        
        self.assertEqual(len(entities), 1)
        entity = entities[0]
        self.assertEqual(entity.id, 'player1')
        self.assertEqual(entity.type, 'PlayerEntity')
        self.assertEqual(entity.name, 'Hero')
        self.assertEqual(entity.components['HealthComponent'].health, 100)


if __name__ == '__main__':
    unittest.main()
