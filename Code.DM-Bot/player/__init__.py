from db_work import DBF_PRIMARY_KEY, DBF_UNIQUE, AsyncDB

from .soul import PlayerSoul

soul_db = AsyncDB(
    db_name="souls",
    db_path="",
    db_config= { 
        "souls": [ 
            ("discord_id", int, (DBF_PRIMARY_KEY | DBF_UNIQUE), None), 
            ("name", str, 0, None) 
        ] 
    }
)


