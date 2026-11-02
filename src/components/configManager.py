import json
import os
from pathlib import Path
from shutil import copy

class configManager:
    def __init__(self):
        if os.name == "nt":
            config_dir = Path(os.getenv("APPDATA")) / "snekye-reader"
        else:
            config_dir = Path(os.getenv("XDG_CONFIG_HOME", Path.home() / '.config')) / "snekye-reader"
        config_dir.mkdir(parents=True,exist_ok=True)
        self.config_file = config_dir / "config.json"

        if not self.config_file.exists():
            copy('default_config.json', self.config_file)

    def load(self):
        with open(self.config_file, "r") as f:
            return json.load(f)

    def save(self, config):
        with open(self.config_file, "w") as f:
            json.dump(config, f, indent=4)