from db_work import AsyncSQLDB

from .soul import PlayerSoul

soul_db = AsyncSQLDB(
    table_name="soul",
    columns= {
        "id": (int, ["PRIMARY KEY AUTOINCREMENT"]),
        "discord_id": (int, ["UNIQUE"]),
        "name": (str, [])
    },
    db_name="soils",
    db_path=""
)
