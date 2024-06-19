import importlib
import os
import shutil
import tempfile
import unittest

from Code.factory import PrototypeError, PrototypeFactory


class TestPrototypeFactory(unittest.TestCase):
    def setUp(self):
        # Создаем временную директорию
        self.test_dir = tempfile.mkdtemp()

        # Создаем файл class_mappings.yml
        self.class_mappings = """
components:
  HealthComponent: "Code.factory.base_component.HealthComponent"
  PositionComponent: "Code.factory.base_component.PositionComponent"

entities:
  PlayerEntity: "Code.factory.base_entity.PlayerEntity"
  EnemyEntity: "Code.factory.base_entity.EnemyEntity"
"""
        self.class_mappings_path = os.path.join(self.test_dir, 'class_mappings.yml')
        with open(self.class_mappings_path, 'w', encoding='utf-8') as f:
            f.write(self.class_mappings)

        # Создаем файл для сущностей
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

        # Создаем экземпляр PrototypeFactory
        self.factory = PrototypeFactory(prototype_dir=self.test_dir)

    def tearDown(self):
        # Удаляем временную директорию после тестов
        shutil.rmtree(self.test_dir)

    def test_create_component(self):
        component_class = self.factory._load_class('Code.factory.base_component.HealthComponent')
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

        entity_class = self.factory._load_class('Code.factory.base_entity.PlayerEntity')
        entity_class.default_values = lambda: {'name': 'Default Player'}
        component_class = self.factory._load_class('Code.factory.base_component.HealthComponent')
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

        entity_class = self.factory._load_class('Code.factory.base_entity.PlayerEntity')
        entity_class.default_values = lambda: {'name': 'Default Player'}
        
        entity = self.factory._create_entity(entity_data, 'dummy_path.yml', 1)
        found_entity = self.factory.find_entity('PlayerEntity', 'player1')
        
        self.assertIsNotNone(found_entity)
        self.assertEqual(found_entity.id, 'player1')

    def test_load_all_entities(self):
        entity_class = self.factory._load_class('Code.factory.base_entity.PlayerEntity')
        entity_class.default_values = lambda: {'name': 'Default Player'}
        component_class = self.factory._load_class('Code.factory.base_component.HealthComponent')
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
