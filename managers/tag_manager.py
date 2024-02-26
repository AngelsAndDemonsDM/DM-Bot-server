from data.tags_data import TagData

class TagsManager:
    def _check_tag(self, tag):
        if not isinstance(tag, TagData):
            raise TypeError("Tag in def(add/rm/find) must be 'TagData' type.")
    
    def _check_array(self, arr_tags):    
        if not isinstance(arr_tags, list):
            raise TypeError("Array tags in def(add/rm/find/sort) must be 'List' type.")
    
    async def find(self, arr_tags, tag):
        self._check_array(arr_tags)
        self._check_tag(tag)
        
        if tag.get_id() is None:
            raise ValueError("Tag has empty ID.")
        
        return tag in arr_tags

    async def add(self, arr_tags, tag):
        if not await self.find(arr_tags, tag):
            arr_tags.append(tag)
            return True
        else:
            return False
        
    async def rm(self, arr_tags, tag):
        if await self.find(arr_tags, tag):
            arr_tags.remove(tag)
            return True
        else:
            return False
        
    async def sort_arr(self, arr_tags):
        self._check_array(arr_tags)
        arr_tags.sort(key=lambda x: x.get_id())
        return True
