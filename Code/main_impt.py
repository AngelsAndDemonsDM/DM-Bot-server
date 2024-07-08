import os

from systems.access_manager import AuthManager
from systems.entity_system import EntityFactory

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

auth_manager = AuthManager()
entity_factory = EntityFactory()
