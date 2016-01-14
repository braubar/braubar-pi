import json

CONFIG_FILE = "../config/config.json"
RECIPE_FILE = "../config/recipe.json"
TEMP_RAW_FILE = "../data/temp.brew"
NEXT_STATE_FILE = "../data/next_state.brew"


class BrewConfig:
    config = None

    def __init__(self):
        self.read_config()

    def read_config(self):
        with open(CONFIG_FILE) as configfile:
            self.config = json.load(configfile)

    def get(self, key):
        return self.config[key]

    def set(self, key, val):
        self.config[key] = val
        with open(CONFIG_FILE, 'w') as configfile:
            json.dump(self.config, configfile, indent=True)