import atexit
import json
from pathlib import Path
from typing import Any, Dict, Union

from misc import GlobalClass
from root_path import ROOT_PATH


class Settings:
    __slots__ = ['_path', '_settings_data']
    
    def __init__(self, file_path: Union[str, Path], file_name: str) -> None:
        if isinstance(file_path, str):
            file_path = Path(file_path)
        
        self._path = file_path / (file_name + ".json")
        
        self._settings_data: Dict[str, Any] = {}
        self._load_settings()
        
        atexit.register(self._save_settings)
    
    def _load_settings(self) -> None:
        if self._path.exists():
            with open(self._path, 'r', encoding='utf-8') as file:
                self._settings_data = json.load(file)
        
        else:
            self._settings_data = {}

    def _save_settings(self) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        with open(self._path, 'w', encoding='utf-8') as file:
            json.dump(self._settings_data, file, ensure_ascii=False, indent=4, sort_keys=True)
    
    def _update_nested_dict(self, original: Dict[str, Any], updates: Dict[str, Any]) -> None:
        for key, value in updates.items():
            if isinstance(value, dict):
                original[key] = original.get(key, {})
                self._update_nested_dict(original[key], value)
            else:
                if key not in original:
                    original[key] = value

    def init_base_settings(self, base_settings: Dict[str, Any]) -> None:
        if not self._settings_data:
            self._settings_data = base_settings
        else:
            self._update_nested_dict(self._settings_data, base_settings)
        
        self._save_settings()
    
    def get_s(self, key: str) -> Any:
        keys = key.split('.')
        data = self._settings_data
        for k in keys:
            if not isinstance(data, dict) or k not in data:
                return None
            data = data[k]
        
        return data
    
    def set_s(self, key: str, value: Any) -> None:
        keys = key.split('.')
        data = self._settings_data
        for k in keys[:-1]:
            if k not in data or not isinstance(data[k], dict):
                data[k] = {}
            data = data[k]
        
        data[keys[-1]] = value

    def get_all(self) -> Dict[str, Any]:
        return self._settings_data

class MainAppSettings(GlobalClass, Settings):
    __slots__ = ['_initialized']
    
    def __init__(self) -> None:
        if self._is_not_initialized():
            super().__init__(ROOT_PATH / "data", "main_app_settings")
