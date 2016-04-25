import json



class BrewConfig:
    config = None

    P = 8000.0
    I = 0.0  # set to zero because cooling is not possible
    D = 350000.0
    MIN = -10000.0
    MAX = 10000.0

    CONFIG_FILE = "../config/config.json"
    RECIPE_FILE = "../config/recipe.json"
    BRAUBAR_QUEUE = "/braubar_queue"
    LOG_BASE = "../log/brewlog_"
    QUEUE_ENCODING = 'utf-8'


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
