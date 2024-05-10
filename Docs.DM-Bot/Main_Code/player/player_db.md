# Документация по файлу `player_db.py`


## `PlayerDB.__getitem__`<br>
Returns information about a user by their Discord ID.<br>
**Args:**<br>
discord_id (str): Discord ID пользователя.<br>
**Returns:**<br>
dict: User information in the form of a dictionary {'Name': name, 'Data': data}.<br>
<br>

## `PlayerDB.add_member`<br>
Add a new member to the database.<br>
**Args:**<br>
discord_id (str): The Discord ID of the member.<br>
name (str): The name of the member.<br>
data (int): The role level of the member.<br>
<br>
