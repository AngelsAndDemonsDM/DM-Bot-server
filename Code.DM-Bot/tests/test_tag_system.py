from etc.tag import Tag, TagsManager


async def test_Tag(logger):
    try:
        tag_data_1 = Tag("test_id")
        tag_data_2 = Tag()  # Проверяем создание объекта без идентификатора
        return False
    except Exception as err:
        logger.debug(err)
    
    # Проверяем, что идентификаторы установлены правильно
    if tag_data_1.id == "test_id":
        logger.debug("Tag test successful.")
        return True
    else:
        logger.debug("Tag test failed.")
        return False

async def test_TagsManager(logger):
    try:
        tags_manager = TagsManager()
    except Exception as err:
        logger.debug(err)
        return False
    
    # Создаем несколько объектов TagData для тестирования
    tag_data_1 = Tag("tag1")
    tag_data_2 = Tag("tag2")
    
    # Создаем список тегов и добавляем теги
    tags_list = []
    tags_manager.add(tags_list, tag_data_1)
    tags_manager.add(tags_list, tag_data_2)
    
    # Проверяем, что теги успешно добавлены
    if len(tags_list) == 2 and tag_data_1 in tags_list and tag_data_2 in tags_list:
        logger.debug("TagsManager add test successful.")
    else:
        logger.debug("TagsManager add test failed.")
        return False
    
    # Удаляем один из тегов
    tags_manager.remove(tags_list, tag_data_2)
    
    # Проверяем, что тег успешно удален
    if len(tags_list) == 1 and tag_data_2 not in tags_list:
        logger.debug("TagsManager remove test successful.")
    else:
        logger.debug("TagsManager remove test failed.")
        return False
    
    # Сортируем список тегов
    tags_manager.sort_arr(tags_list)
    
    # Проверяем, что список тегов отсортирован по идентификаторам
    sorted_ids = [tag.id for tag in tags_list]
    if sorted_ids == sorted(sorted_ids):
        logger.debug("TagsManager sort_arr test successful.")
        return True
    else:
        logger.debug("TagsManager sort_arr test failed.")
        return False
