import json
import os

class SettingsService:
    def __init__(self):
        self.config_file = "configs.json"

    def _load_config_data(self) -> dict:
        default_data = {"API_Key": ""}
        if not os.path.exists(self.config_file):
            return default_data
        try:
            with open(self.config_file, "r") as f:
                data = json.load(f)
                if "API_Key" not in data: 
                    data["API_Key"] = ""
                return data
        except (json.JSONDecodeError, FileNotFoundError):
            return default_data

    def _save_config_data(self, data: dict) -> None:
        with open(self.config_file, "w") as f:
            json.dump(data, f, indent=4)

    def save_api_key(self, key: str) -> None:
        data = self._load_config_data()
        data["API_Key"] = key
        self._save_config_data(data)

    def get_api_key(self) -> str:
        data = self._load_config_data()
        return data.get("API_Key", "")