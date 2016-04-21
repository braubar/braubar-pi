import json



class BrewConfig:
    config = None

    P = 8000.0
    I = 0.0  # set to zero because cooling is not possible
    D = 350000.0
    MIN = -10.0
    MAX = 10.0

    CONFIG_FILE = "../config/config.json"
    RECIPE_FILE = "../config/recipe.json"
    TEMP_RAW_FILE = "../data/temp.brew"
    NEXT_STATE_FILE = "../data/next_state.brew"
    LOG_BASE = "../log/brewlog_"

    def __init__(self):
        self.read_config()

    def read_config(self):
        with open(BrewConfig.CONFIG_FILE) as configfile:
            self.config = json.load(configfile)

    def get(self, key):
        return self.config[key]

    def set(self, key, val):
        self.config[key] = val
        with open(BrewConfig.CONFIG_FILE, 'w') as configfile:
            json.dump(self.config, configfile, indent=True)
