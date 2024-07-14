import os

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

from systems.access_system import AuthManager
from systems.entity_system import EntityFactory

auth_manager = AuthManager()
entity_factory = EntityFactory()
