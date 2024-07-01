from db_work import AsyncDB
from factory import PrototypeFactory
from texture_manager import TextureSystem

soul_db = AsyncDB(
    db_name="souls",
    db_path="data",
    db_config= { 
        "souls": [ 
            ("discord_id", int, (AsyncDB.PRIMARY_KEY | AsyncDB.UNIQUE), None), 
            ("name", str, 0, None) 
        ] 
    }
)

sprite_system = TextureSystem('Sprites')
prototype_factory = PrototypeFactory()
