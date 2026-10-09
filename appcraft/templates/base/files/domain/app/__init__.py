from enum import Enum


class Environment(str, Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"


class Theme(str, Enum):
    DARK = "dark"
    LIGHT = "light"
