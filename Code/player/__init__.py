from db_work import AsyncDB
from player.soul import PlayerSoul

soul_db = AsyncDB(
    db_name="souls",
    db_path="",
    db_config= { 
        "souls": [ 
            ("discord_id", int, (AsyncDB.PRIMARY_KEY | AsyncDB.UNIQUE), None), 
            ("name", str, 0, None) 
        ] 
    }
)
