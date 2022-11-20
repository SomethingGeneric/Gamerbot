import os

# Nonstandard to avoid depend loop
from logger import BotLogger

syslog = BotLogger("system_log.txt")


def check(fn):
    if os.path.exists(fn):
        return True
    else:
        return False


class ConfigManager:
    def __init__(self, fn, logging=True):
        self.fn = fn
        self.config = {}
        if not check(fn):
            if logging:
                syslog.log("Config", "No config found!")
        else:
            if logging:
                syslog.log("Config", "----- Loading config values -----")
            with open(fn) as f:
                config_lines = f.read().split("\n")
            for line in config_lines:
                if line != "" and line != "\n":
                    if line[0] != "#":
                        bits = line.split(":")
                        key = bits[0]
                        val = bits[1]
                        if logging:
                            syslog.log("Config", "Added " + key + ": " + val)
                        self.config[key] = val
            self.is_logging = logging

    def reload_config(self):
        if not check(self.fn):
            if self.logging:
                syslog.log("Config", "No config found!")
        else:
            if self.logging:
                syslog.log("Config", "----- Loading config values -----")
            with open(self.fn) as f:
                config_lines = f.read().split("\n")
            for line in config_lines:
                if line != "" and line != "\n":
                    if line[0] != "#":
                        bits = line.split(":")
                        key = bits[0]
                        val = bits[1]
                        if self.logging:
                            syslog.log("Config", "Added " + key + ": " + val)
                        self.config[key] = val

    def get(self, key):
        if key in self.config:
            return self.config[key].replace("//", "://")
        else:
            return "Not found"

    def get_as_int(self, key):
        if key in self.config:
            return int(self.config[key])
        else:
            return 0

    def get_as_bool(self, key):
        if key in self.config:
            result = self.config[key]
            if result == "true" or result == "True":
                return True
            else:
                return False
        else:
            return False

    def get_as_list(self, key):
        if key in self.config:
            if "," in self.config[key]:
                return self.config[key].split(",")
            else:
                return [self.config[key]]
        else:
            return None

    def get_as_int_list(self, key):
        if key in self.config:
            if "," in self.config[key]:
                data = self.config[key].split(",")
                new_data = []
                for item in data:
                    new_data.append(int(item))
                return new_data
            else:
                return [int(self.config[key])]
        else:
            return [0]
