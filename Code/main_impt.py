from db_work import AsyncDB
from factory import PrototypeFactory

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

prototype_factory = PrototypeFactory()
