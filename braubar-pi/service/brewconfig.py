import json
import os


class BrewConfig:
    config = None

    def __init__(self):
        print(os.getcwd())
        self.read_config()

    def read_config(self):
        with open("data/config.json") as configfile:
            self.config = json.load(configfile)

    def get(self, key):
        return self.config[key]

    def set(self, key, val):
        self.config[key] = val
        with open("data/config.json", 'w') as configfile:
            json.dump(self.config, configfile, indent=True)
